import pygame
import random as rand
import math
import constants as const



class Wall:
    def __init__(self, x, y):
        x = rand.randrange(1,1200)
        y = rand.randrange(1,600)
        
        self.x = x
        self.y = y
        self.radius = const.WALL_SIZE
        self.speed = const.WALL_SPEED*0
        self.mass = const.WALL_MASS
        self.angle = 0
        
    def move(self, time_delta):
        '''
        self.x =  0
        self.y =  0
        #self.speed *= const.FRICTION
        '''
        self.x += math.sin(self.angle) * self.speed * time_delta * 0
        self.y -= math.cos(self.angle) * self.speed * time_delta * 0

    def check_boundary(self, width, height):
        # right side
        if self.x + self.radius > width:
            self.x = 2 * (width - self.radius) - self.x
            self.angle = -self.angle

        # left side
        elif self.x - self.radius < 0:
            self.x = 2 * self.radius - self.x
            self.angle = -self.angle

        # bottom
        if self.y + self.radius > height:
            self.y = 2 * (height - self.radius) - self.y
            self.angle = math.pi - self.angle

        # top
        elif self.y - self.radius < 0:
            self.y = 2 * self.radius - self.y
            self.angle = math.pi - self.angle
        
        
    def add_vectors(self, angle1, length1, angle2, length2):
        x = math.sin(angle1) * length1 + math.sin(angle2) * length2
        y = math.cos(angle1) * length1 + math.cos(angle2) * length2

        length = math.hypot(x, y)
        angle = math.pi / 2 - math.atan2(y, x)
        return angle, length
    '''
    def collision_paddle(self, paddle):
        """
        Checks collision between circles using the distance formula:
        distance = sqrt(dx**2 + dy**2)
        """
        dx = self.x - paddle.x
        dy = self.y - paddle.y

        # distance between the centers of the circle
        distance = math.hypot(dx, dy)

        # no collision takes place.
        if distance > self.radius + paddle.radius:
            return False

        # calculates angle of projection.
        tangent = math.atan2(dy, dx)
        temp_angle = math.pi / 2 + tangent
        total_mass = self.mass + paddle.mass

        # The new vector for puck formed after collision.
        vec_a = (self.angle, self.speed * (self.mass - paddle.mass) / total_mass)
        vec_b = (temp_angle, 2 * paddle.speed * paddle.mass / total_mass)

        (self.angle, self.speed) = self.add_vectors(*vec_a, *vec_b)

        # speed should never exceed a certain limit.
        if self.speed > const.MAX_SPEED:
            self.speed = const.MAX_SPEED

        # new vector for paddle without changing the speed.
        vec_a = (paddle.angle, paddle.speed * (paddle.mass - self.mass) / total_mass)
        vec_b = (temp_angle + math.pi, 2 * self.speed * self.mass / total_mass)

        temp_speed = paddle.speed
        (paddle.angle, paddle.speed) = self.add_vectors(*vec_a, *vec_b)
        paddle.speed = temp_speed

        # To prevent puck and paddle from sticking.
        offset = 0.5 * (self.radius + paddle.radius - distance + 1)
        self.x += math.sin(temp_angle) * offset
        self.y -= math.cos(temp_angle) * offset
        paddle.x -= math.sin(temp_angle) * offset
        paddle.y += math.cos(temp_angle) * offset
        return True
    '''
    #paddle => puck으로 변경
    def collision_paddle(self, puck):
        """
        Checks collision between circles using the distance formula:
        distance = sqrt(dx**2 + dy**2)
        """
        dx = self.x - puck.x
        dy = self.y - puck.y

        # distance between the centers of the circle
        distance = math.hypot(dx, dy)

        # no collision takes place.
        if distance > self.radius + puck.radius:
            return False

        # calculates angle of projection.
        tangent = math.atan2(dy, dx)
        temp_angle = math.pi / 2 + tangent
        total_mass = self.mass + puck.mass

        # The new vector for puck formed after collision.
        vec_a = (self.angle, self.speed * (self.mass - puck.mass) / total_mass)
        vec_b = (temp_angle, 2 * puck.speed * puck.mass / total_mass)

        (self.angle, self.speed) = self.add_vectors(*vec_a, *vec_b)

        # speed should never exceed a certain limit.
        if self.speed > const.MAX_SPEED:
            self.speed = const.MAX_SPEED

        # new vector for paddle without changing the speed.
        vec_a = (puck.angle, puck.speed * (puck.mass - self.mass) / total_mass)
        vec_b = (temp_angle + math.pi, 2 * self.speed * self.mass / total_mass)

        temp_speed = puck.speed
        (puck.angle, puck.speed) = self.add_vectors(*vec_a, *vec_b)
        puck.speed = temp_speed

        # To prevent puck and paddle from sticking.
        offset = 0.5 * (self.radius + puck.radius - distance + 1)
        self.x += math.sin(temp_angle) * offset
        self.y -= math.cos(temp_angle) * offset
        puck.x -= math.sin(temp_angle) * offset
        puck.y += math.cos(temp_angle) * offset
        return True


    def round_reset(self, player):
        x = rand.randrange(1,1200)
        y = rand.randrange(1,600)
        if player == 1:
            self.x = x
        if player == 2:
            self.x = x
        self.y = y
        self.angle = 0
        self.speed = 0

    def reset(self, speed, player):
        if player == 1:
            self.angle = rand.uniform(-math.pi, 0)
        elif player == 2:
            self.angle = rand.uniform(0, math.pi)
        self.speed = speed*0
        x = rand.randrange(1,1200)
        y = rand.randrange(1,600)
        self.x = x
        self.y = y

    def end_reset(self, speed):
        self.angle = 0
        self.speed = speed*0
        x = rand.randrange(1,1200)
        y = rand.randrange(1,600)
        self.x = x
        self.y = y

    def draw(self, screen):
        pygame.draw.circle(screen, const.GRAY, (int(self.x), int(self.y)), self.radius)

    def get_pos(self):
        print (self.x, self.y)

    def collision_with_paddle(self,paddle):#패들이랑 장애물이랑 충돌처리해주는 메서드
        """
        Checks collision between circles using the distance formula:
        distance = sqrt(dx**2 + dy**2)
        """
        dx = self.x - paddle.x
        dy = self.y - paddle.y

        # distance between the centers of the circle
        distance = math.hypot(dx, dy)

        # no collision takes place.
        if distance > self.radius + paddle.radius:
            return False

        # calculates angle of projection.
        tangent = math.atan2(dy, dx)
        temp_angle = math.pi / 2 + tangent
        total_mass = self.mass + paddle.mass

        # The new vector for puck formed after collision.
        vec_a = (self.angle, self.speed * (self.mass - paddle.mass) / total_mass)
        vec_b = (temp_angle, 2 * paddle.speed * paddle.mass / total_mass)

        ow_angle=self.angle
        ow_speed=self.speed
        (self.angle, self.speed) = self.add_vectors(*vec_a, *vec_b)
        self.angle=ow_angle
        self.speed=ow_speed

        # speed should never exceed a certain limit.
        if self.speed > const.MAX_SPEED:
            self.speed = const.MAX_SPEED

        # new vector for paddle without changing the speed.
        vec_a = (paddle.angle, paddle.speed * (paddle.mass - self.mass) / total_mass)
        vec_b = (temp_angle + math.pi, 2 * self.speed * self.mass / total_mass)

        temp_speed = paddle.speed
        (paddle.angle, paddle.speed) = self.add_vectors(*vec_a, *vec_b)
        paddle.speed = temp_speed

        # To prevent puck and paddle from sticking.
        offset = 0.5 * (self.radius + paddle.radius - distance + 1)
        self.x += math.sin(temp_angle) * offset
        self.y -= math.cos(temp_angle) * offset
        paddle.x -= math.sin(temp_angle) * offset
        paddle.y += math.cos(temp_angle) * offset
        return True

