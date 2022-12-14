import numpy

class LineFollowerBot:
    def __init__(self, pb_client, model_file_name, starting_position):
        self.pb_client = pb_client
        
        orientation = self._to_quaternion(starting_position[1][0], 0.0, 0.0)
     
        self.bot_model = self.pb_client.loadURDF(model_file_name, basePosition = starting_position[0], baseOrientation = orientation)
        
        self.speed_max_rpm  = 1000.0

        self.speed_max = self.speed_max_rpm*2.0*3.141592654/60.0

        self.left_velocity = 0.0
        self.right_velocity = 0.0
        
        self.left_wheel_joint   = 0
        self.right_wheel_joint  = 1

        self.set_throttle(0.0, 0.0)
        

    def set_throttle(self, left_power, right_power, inertia = 0.8):
        self.left_velocity   =  inertia*self.left_velocity  + (1.0 - inertia)*left_power
        self.right_velocity  =  inertia*self.right_velocity + (1.0 - inertia)*right_power

        self.set_velocity(self.left_velocity, self.right_velocity)
    
    def set_velocity(self, left_velocity, right_velocity):
        vl  = numpy.clip(left_velocity, -1.0, 1.0)*self.speed_max
        vr  = numpy.clip(right_velocity, -1.0, 1.0)*self.speed_max

        self._set_wheel_velocity(vl, vr)


    def get_wheel_position(self):
        l_pos, l_vel, l_react, l_torque = self.pb_client.getJointState(self.bot_model, self.left_wheel_joint)
        r_pos, r_vel, r_react, r_torque = self.pb_client.getJointState(self.bot_model, self.right_wheel_joint)
        """for i in range(10):
            print(self.pb_client.getJointInfo(self.bot_model, i))"""
        return l_pos, r_pos
    
    def get_sensor_positions(self):
        left_pos = self.pb_client.getLinkState(self.bot_model, 3)
        left_pos = left_pos[0]
        left_pos = left_pos[0], left_pos[1]
        middle_pos = self.pb_client.getLinkState(self.bot_model, 4)
        middle_pos = middle_pos[0]
        middle_pos = middle_pos[0], middle_pos[1]
        right_pos = self.pb_client.getLinkState(self.bot_model, 5)
        right_pos = right_pos[0]
        right_pos = right_pos[0], right_pos[1]
        return left_pos, middle_pos, right_pos

    def get_wheel_torque(self):
        l_pos, l_vel, l_react, l_torque = self.pb_client.getJointState(self.bot_model, self.left_wheel_joint)
        r_pos, r_vel, r_react, r_torque = self.pb_client.getJointState(self.bot_model, self.right_wheel_joint)
        return l_torque, r_torque

    def get_wheel_velocity(self):
        l_pos, l_vel, l_react, l_torque = self.pb_client.getJointState(self.bot_model, self.left_wheel_joint)
        r_pos, r_vel, r_react, r_torque = self.pb_client.getJointState(self.bot_model, self.right_wheel_joint)
        return l_vel, r_vel

    def get_position(self):
        position, orientation = self.pb_client.getBasePositionAndOrientation(self.bot_model)
        x, y, z = position
        orientation = self.pb_client.getEulerFromQuaternion(orientation)
        pitch, roll, yaw = orientation
        return x, y, z, pitch, roll, yaw

    def get_position_2(self):
        position, orientation, _, _, _, _ = self.pb_client.getLinkState(self.bot_model, 4)
        x, y, z = position
        orientation = self.pb_client.getEulerFromQuaternion(orientation)
        pitch, roll, yaw = orientation
        return x, y, z, pitch, roll, yaw

    def _set_wheel_velocity(self, left_velocity, right_velocity):

        self.pb_client.setJointMotorControl2(self.bot_model,
                                             jointIndex =   self.left_wheel_joint,
                                             controlMode=   self.pb_client.VELOCITY_CONTROL,
                                             targetVelocity      =   left_velocity)

        self.pb_client.setJointMotorControl2(self.bot_model,
                                             jointIndex =   self.right_wheel_joint,
                                             controlMode=   self.pb_client.VELOCITY_CONTROL,
                                             targetVelocity      =   right_velocity)
    
    def _to_quaternion(self, yaw, pitch, roll):
        cy = numpy.cos(yaw * 0.5)
        sy = numpy.sin(yaw * 0.5)
        cp = numpy.cos(pitch * 0.5)
        sp = numpy.sin(pitch * 0.5)
        cr = numpy.cos(roll * 0.5)
        sr = numpy.sin(roll * 0.5)

        x = cy * cp * sr - sy * sp * cr
        y = sy * cp * sr + cy * sp * cr
        z = sy * cp * cr - cy * sp * sr
        w = cy * cp * cr + sy * sp * sr

        return x, y, z, w



    def get_image(self, yaw, pitch, roll, distance, target_x, target_y, target_z, width = 512, height = 512, fov = 120):
        

        vm = self.pb_client.computeViewMatrixFromYawPitchRoll([target_x, target_y, target_z], distance, yaw, pitch, roll, 2)


        pm = self.pb_client.computeProjectionMatrixFOV(fov=fov,
                                                       aspect=width / height,
                                                       nearVal=0.0001,
                                                       farVal=10.1) 

        w, h, rgb, deth, seg = self.pb_client.getCameraImage(width=width,
                                                             height=height,
                                                             viewMatrix=vm,
                                                             projectionMatrix=pm,
                                                             renderer=self.pb_client.ER_BULLET_HARDWARE_OPENGL)

        rgb = numpy.array(rgb)
        rgb = rgb[:, :, :3]
       
        return rgb