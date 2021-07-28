import math

from props import getNode
from auracore import wgs84

import comms.events
import control.route
from mission.task.task import Task
import mission.task.state

d2r = math.pi / 180.0
r2d = 180.0 / math.pi
ft2m = 0.3048
m2ft = 1.0 / ft2m

class Land(Task):
    def __init__(self, config_node):
        Task.__init__(self)
        self.task_node = getNode("/task", True)
        self.home_node = getNode("/task/home", True)
        self.land_node = getNode("/task/land", True)
        self.circle_node = getNode("/task/circle", True)
        self.route_node = getNode("/task/route", True)
        self.ap_node = getNode("/autopilot", True)
        self.nav_node = getNode("/navigation", True)
        self.pos_node = getNode("/position", True)
        self.vel_node = getNode("/velocity", True)
        self.orient_node = getNode("/orientation", True)
        self.flight_node = getNode("/controls/flight", True)
        self.engine_node = getNode("/controls/engine", True)
        self.imu_node = getNode("/sensors/imu", True)
        self.targets_node = getNode("/autopilot/targets", True)
        self.pilot_node = getNode("/sensors/pilot_input", True)

        # get task configuration parameters
        self.name = config_node.getString("name")
        self.nickname = config_node.getString("nickname")
        self.lateral_offset_m = config_node.getDouble("lateral_offset_m")
        self.glideslope_deg = config_node.getDouble("glideslope_deg")
        if self.glideslope_deg < 0.01:
            self.glideslope_deg = 6.0
        self.turn_radius_m = config_node.getDouble("turn_radius_m")
        if self.turn_radius_m < 1.0:
            self.turn_radius_m = 75.0
        self.direction = config_node.getString("direction")
        if self.direction == "":
            self.direction = "left"
        self.extend_final_leg_m = config_node.getDouble("extend_final_leg_m")
        self.alt_bias_ft = config_node.getDouble("alt_bias_ft")
        self.approach_speed_kt = config_node.getDouble("approach_speed_kt")
        if self.approach_speed_kt < 0.1:
            self.approach_speed_kt = 25.0
        self.flare_pitch_deg = config_node.getDouble("flare_pitch_deg")
        self.flare_seconds = config_node.getDouble("flare_seconds")
        if self.flare_seconds < 0.1:
            self.flare_seconds = 5.0
        if config_node.hasChild("flaps"):
            self.flaps = config_node.getDouble("flaps")
        else:
            self.flaps = 0.0

        # copy to /task/land
        self.land_node.setDouble("lateral_offset_m", self.lateral_offset_m)
        self.land_node.setDouble("glideslope_deg", self.glideslope_deg)
        self.land_node.setDouble("turn_radius_m", self.turn_radius_m)
        self.land_node.setString("direction", self.direction)
        self.land_node.setDouble("extend_final_leg_m", self.extend_final_leg_m)
        self.land_node.setDouble("altitude_bias_ft", self.alt_bias_ft)
        self.land_node.setDouble("approach_speed_kt", self.approach_speed_kt)
        self.land_node.setDouble("flare_pitch_deg", self.flare_pitch_deg)
        self.land_node.setDouble("flare_seconds", self.flare_seconds)

        self.side = -1.0
        self.flare = False
        self.flare_start_time = 0.0
        self.approach_throttle = 0.0
        self.approach_pitch = 0.0
        self.flare_pitch_range = 0.0
        self.final_heading_deg = 0.0
        self.final_leg_m = 0.0
        self.dist_rem_m = 0.0
        self.circle_capture = False
        self.gs_capture = False

    def activate(self):
        if not self.active:
            # build the approach with the current property tree values
            self.build_approach()

        # Save existing state
        mission.task.state.save(modes=True, circle=True, targets=True)
        
        self.ap_node.setString("mode", "basic+tecs")
        self.nav_node.setString("mode", "circle")
        self.targets_node.setDouble("airspeed_kt",
                                   self.land_node.getDouble("approach_speed_kt"))
        self.flight_node.setDouble("flaps_setpoint", self.flaps)

        # start at the beginning of the route (in case we inherit a
        # partially flown approach from earlier in the flight)
        # approach_mgr.restart() # FIXME
        self.circle_capture = False
        self.gs_capture = False
        self.flare = False

        self.active = True
        comms.events.log("mission", "land")

    def cart2polar(self, x, y):
        # fixme: if display_on:
        #    printf("approach %0f %0f\n", x, y);
        dist = math.sqrt(x*x + y*y)
        deg = math.atan2(x, y) * r2d
        return (dist, deg)

    def polar2cart(self, deg, dist):
        x = dist * math.sin(deg * d2r)
        y = dist * math.cos(deg * d2r)
        return (x, y)

    def update(self, dt):
        if not self.active:
            return False

        self.glideslope_rad = self.land_node.getDouble("glideslope_deg") * d2r
        self.extend_final_leg_m = self.land_node.getDouble("extend_final_leg_m")
        self.alt_bias_ft = self.land_node.getDouble("altitude_bias_ft")

        # add ability for pilot to bias the glideslope altitude using
        # stick/elevator (negative elevator is up.)
        self.alt_bias_ft += -self.pilot_node.getDouble("elevator") * 25.0

        # compute minimum 'safe' altitude
        safe_dist_m = math.pi * self.turn_radius_m + self.final_leg_m
        safe_alt_ft = safe_dist_m * math.tan(self.glideslope_rad) * m2ft \
                      + self.alt_bias_ft

        # position on circle descent
        circle_pos = 0

        mode = self.nav_node.getString('mode')
        if mode == 'circle':
            # circle descent portion of the approach
            pos_lon = self.pos_node.getDouble("longitude_deg")
            pos_lat = self.pos_node.getDouble("latitude_deg")
            center_lon = self.circle_node.getDouble("longitude_deg")
            center_lat = self.circle_node.getDouble("latitude_deg")
            # compute course and distance to center of target circle
            (course_deg, rev_deg, cur_dist_m) = \
                wgs84.geo_inverse( center_lat, center_lon, pos_lat, pos_lon )
            # test for circle capture
            if not self.circle_capture:
                fraction = abs(cur_dist_m / self.turn_radius_m)
                #print 'heading to circle:', err, fraction
                if fraction > 0.75 and fraction < 1.25:
                    # within 25% of target circle radius, call the
                    # circle capture
                    comms.events.log("land", "descent circle capture")
                    self.circle_capture = True

            # compute portion of circle remaining to tangent point
            current_crs = course_deg + self.side * 90
            if current_crs > 360.0: current_crs -= 360.0
            if current_crs < 0.0: current_crs += 360.0
            circle_pos = current_crs - self.final_heading_deg
            if circle_pos < -180.0: circle_pos += 360.0
            if circle_pos > 180.0: circle_pos -= 360.0
            # print 'circle_pos:', self.orient_node.getDouble('groundtrack_deg'), current_crs, self.final_heading_deg, circle_pos
            angle_rem_rad = math.pi
            if self.circle_capture and circle_pos > -10:
                # circling, captured circle, and within 180 degrees
                # towards tangent point (or just slightly passed)
                angle_rem_rad = circle_pos * math.pi / 180.0

            # distance to edge of circle + remaining circumference of
            # circle + final approach leg
            self.dist_rem_m = (cur_dist_m - self.turn_radius_m) \
                              + angle_rem_rad * self.turn_radius_m \
                              + self.final_leg_m
            # print 'circle:', self.dist_rem_m, self.turn_radius_m, self.final_leg_m, cur_dist_m
            if self.circle_capture and self.gs_capture:
                # we are on the circle and on the glide slope, lets
                # look for our lateral exit point
                if abs(circle_pos) <= 10.0:
                    comms.events.log("land", "transition to final")
                    self.nav_node.setString("mode", "route")
        else:
            # on final approach
            if control.route.dist_valid:
                self.dist_rem_m = self.route_node.getDouble("dist_remaining_m")

        # compute glideslope/target elevation
        alt_m = self.dist_rem_m * math.tan(self.glideslope_rad)
        # print ' ', mode, "dist = %.1f alt = %.1f" % (self.dist_rem_m, alt_m)

        # Compute target altitude.
        cur_alt = self.pos_node.getDouble("altitude_agl_ft")
        cur_target_alt = self.targets_node.getDouble("altitude_agl_ft")
        new_target_alt = alt_m * m2ft + self.alt_bias_ft

        # prior to glide slope capture, never allow target altitude
        # lower than safe altitude
        if not self.gs_capture:
            # print 'safe:', safe_alt_ft, 'new:', new_target_alt
            if new_target_alt < safe_alt_ft:
                new_target_alt = safe_alt_ft

        # We want to avoid wasting energy needlessly gaining altitude.
        # Once the approach has started, never raise the target
        # altitude.
        if new_target_alt > cur_target_alt:
            new_target_alt = cur_target_alt

        self.targets_node.setDouble("altitude_agl_ft", new_target_alt)

        # compute error metrics relative to ideal glide slope
        alt_error_ft = cur_alt - (alt_m * m2ft + self.alt_bias_ft)
        gs_error = math.atan2(alt_error_ft * ft2m, self.dist_rem_m) * r2d
        #print "alt_error_ft = %.1f" % alt_error_ft, "gs err = %.1f" % gs_error

        if self.circle_capture and not self.gs_capture:
            # on the circle, but haven't intercepted gs
            #print 'waiting for gs intercept'
            if gs_error <= 1.0 and circle_pos >= 0:
                # 1 degree or less glide slope error and on the 2nd
                # half of the circle, call the gs captured
                comms.events.log("land", "glide slope capture")
                self.gs_capture = True

        # compute time to touchdown at current ground speed (assuming the
        # navigation system has lined us up properly
        ground_speed_ms = self.vel_node.getDouble("groundspeed_ms")
        if ground_speed_ms > 0.01:
            seconds_to_touchdown = self.dist_rem_m / ground_speed_ms
        else:
            seconds_to_touchdown = 1000.0 # lots

        #print "dist_rem_m = %.1f gs = %.1f secs = %.1f" % \
        #    (self.dist_rem_m, ground_speed_ms, seconds_to_touchdown)

        # approach_speed_kt = approach_speed_node.getDouble()
        self.flare_pitch_deg = self.land_node.getDouble("flare_pitch_deg")
        self.flare_seconds = self.land_node.getDouble("flare_seconds")

        if seconds_to_touchdown <= self.flare_seconds and not self.flare:
            # within x seconds of touchdown horizontally.  Note these
            # are padded numbers because we don't know the truth
            # exactly ... we could easily be closer or lower or
            # further or higher.  Our flare strategy is to smoothly
            # pull throttle to idle, while smoothly pitching to the
            # target flare pitch (as configured in the task
            # definition.)
            comms.events.log("land", "start flare")
            self.flare = True
            self.flare_start_time = self.imu_node.getDouble("timestamp")
            self.approach_throttle = self.engine_node.getDouble("throttle")
            self.approach_pitch = self.targets_node.getDouble("pitch_deg")
            self.flare_pitch_range = self.approach_pitch - self.flare_pitch_deg
            self.ap_node.setString("mode", "basic")

        if self.flare:
            if self.flare_seconds > 0.01:
                elapsed = self.imu_node.getDouble("timestamp") - self.flare_start_time
                percent = elapsed / self.flare_seconds
                if percent > 1.0:
                    percent = 1.0
                self.targets_node.setDouble("pitch_deg",
                                           self.approach_pitch
                                           - percent * self.flare_pitch_range)
                self.engine_node.setDouble("throttle",
                                          self.approach_throttle * (1.0 - percent))
                #printf("FLARE: elapsed=%.1f percent=%.2f speed=%.1f throttle=%.1f",
                #       elapsed, percent,
                #       approach_speed_kt - percent * self.flare_pitch_range,
                #       self.approach_throttle * (1.0 - percent))
            else:
                # printf("FLARE!!!!\n")
                self.targets_node.setDouble("pitch_deg", self.flare_pitch_deg)
                self.engine_node.setDouble("throttle", 0.0)

        # if ( display_on ) {
        #    printf("land dist = %.0f target alt = %.0f\n",
        #           self.dist_rem_m, alt_m * SG_METER_TO_FEET + self.alt_bias_ft)

    def is_complete(self):
        return False

        # Fixme: this would make more sense if we popped all the other tasks
        # off the stack first, the pushed land on the stack
        # ... otherwise we jump back to route or circle or whatever we
        # were doing before when this finishes.
        # Maybe request idle task? or pop all task and the push idle task?
        if self.task_node.getBool("is_airborne"):
            return False
        else:
            # FIXME: task is to land and we are on the ground, let's say we
            # are all done.
            return True;

    def close(self):
        # restore the previous state
        mission.task.state.restore()
        self.flight_node.setDouble("flaps_setpoint", 0.0)
        
        self.active = False
        return True

    def build_approach(self):
        # Setup a descending circle tangent to the final approach
        # path.  The touchdown point is 'home' and the final heading
        # is home azimuth.  The final approach route is simply two
        # points.  A circle decent if flown until the glideslope is
        # captured and then at the correct exit point the task
        # switches to route following mode.  Altitude/decent is
        # managed by this task.

        # fetch parameters
        self.turn_radius_m = self.land_node.getDouble("turn_radius_m")
        self.extend_final_leg_m = self.land_node.getDouble("extend_final_leg_m")
        self.lateral_offset_m = self.land_node.getDouble("lateral_offset_m")
        self.side = -1.0
        dir = self.land_node.getString("direction")
        if dir == "left":
            self.side = -1.0
        elif dir == "right":
            self.side = 1.0
        self.final_heading_deg = self.home_node.getDouble("azimuth_deg")

        # final leg length
        self.final_leg_m = 2.0 * self.turn_radius_m + self.extend_final_leg_m

        # compute center of decending circle
        x = self.turn_radius_m * self.side - self.lateral_offset_m * self.side
        y = 2 * self.turn_radius_m + self.extend_final_leg_m
        (offset_dist, offset_deg) = self.cart2polar(x, -y)
        circle_offset_deg = self.final_heading_deg + offset_deg
        if circle_offset_deg < 0.0:
            circle_offset_deg += 360.0
        if circle_offset_deg > 360.0:
            circle_offset_deg -= 360.0
        #print "circle_offset_deg:", circle_offset_deg
        (cc_lat, cc_lon, az2) = \
            wgs84.geo_direct( self.home_node.getDouble("latitude_deg"),
                              self.home_node.getDouble("longitude_deg"),
                              circle_offset_deg, offset_dist )

        # configure circle task
        self.circle_node.setDouble('latitude_deg', cc_lat)
        self.circle_node.setDouble('longitude_deg', cc_lon)
        self.circle_node.setString('direction', dir)
        self.circle_node.setDouble('radius_m', self.turn_radius_m)

        # create and request approach route
        # start of final leg point
        (dist, deg) = self.cart2polar(-self.lateral_offset_m * self.side,
                                      -self.final_leg_m)
        route_request = "0,%.2f,%.2f,-" % (dist, deg)
        # touchdown point
        (dist, deg) = self.cart2polar(-self.lateral_offset_m * self.side, 0.0)
        route_request += ",0,%.2f,%.2f,-" % (dist, deg)

        # set route request and route modes
        self.route_node.setString("route_request", route_request)
        self.route_node.setString("start_mode", "first_wpt")
        self.route_node.setString("follow_mode", "leader")
        self.route_node.setString("completion_mode", "extend_last_leg")

        # seed route dist_remaining_m value so it is not zero or left
        # over from previous route.
        self.route_node.setDouble("dist_remaining_m", self.final_leg_m)

        return True
