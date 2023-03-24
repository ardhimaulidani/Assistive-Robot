import pygame 
import pygame.freetype
import os

from ffpyplayer.player import MediaPlayer
from ffpyplayer.tools import set_loglevel
from pymediainfo import MediaInfo
from errno import ENOENT

from aruco_read import aruco
import cv2
import numpy as np

from itertools import cycle

class Start:
  def __init__(self):
    self.BLINK_EVENT = pygame.USEREVENT + 1

    self.GAME_FONT = pygame.freetype.Font("bin/prstartk.ttf", 13)
    self.title_surf, self.title_rect = self.GAME_FONT.render("ASSISTIVE-ROBOT", (255,255,255), (0,0,0), 0, 0, 24)
    self.start_surf, self.start_rect = self.GAME_FONT.render("PRESS START BUTTON", (255,255,255), (0,0,0), 0, 0, 14)
    self.copyright_surf, self.copyright_rect = self.GAME_FONT.render("\xa9 2023 ADINDA", (255,255,255), (0,0,0), 0, 0, 10)

    self.robot_surf = pygame.image.load("bin/robot.png").convert()
    self.robot_surf = pygame.transform.scale(self.robot_surf, (135, 175))

    self.off_start_surf = pygame.Surface(self.start_rect.size)
    self.off_start_surf.fill(pygame.Color("black"))
    
    self.blink_list = cycle([self.start_surf, self.off_start_surf])
    self.blink_surf = next(self.blink_list)
    pygame.time.set_timer(self.BLINK_EVENT, 1000)

  def draw(self, surf: pygame.Surface, pos: tuple, force_draw: bool = True) -> bool:
    surf.blit(self.robot_surf, ((480-135)/2,(320-175)/2))
    surf.blit(self.title_surf, ((480-self.title_rect[2])/2,(100-self.title_rect[3])/2))
    surf.blit(self.blink_surf, ((480-self.start_rect[2])/2,260))
    surf.blit(self.copyright_surf, ((480-self.copyright_rect[2])/2,305))
    return True         

class Tutorial:
  def __init__(self):
    self.GAME_FONT = pygame.freetype.Font("bin/prstartk.ttf", 16)
    self.title_surf, self.title_rect = self.GAME_FONT.render("How to Move:", (255,255,255), (0,0,0), 0, 0, 16)

    self.arrow_surf = pygame.image.load("bin/arrow.png").convert()
    self.arrow_surf = pygame.transform.scale(self.arrow_surf, (150, 100))

    self.joystick_surf = pygame.image.load("bin/joystick.png").convert()
    self.joystick_surf = pygame.transform.scale(self.joystick_surf, (100, 115))
    
    self.cross_surf = pygame.image.load("bin/cross.png").convert()
    self.cross_surf = pygame.transform.scale(self.cross_surf, (23, 23))

    self.text_surf, self.text_rect = self.GAME_FONT.render("Press    to Continue", (255,255,255), (0,0,0), 0, 0, 12)
    self.analogtext_surf, self.analogtext_rect = self.GAME_FONT.render("Left Analog", (255,255,255), (0,0,0), 0, 0, 12)
    self.arrowtext_surf, self.arrowtext_rect = self.GAME_FONT.render("Arrow Keys", (255,255,255), (0,0,0), 0, 0, 12)

  def draw(self, surf: pygame.Surface, pos: tuple, force_draw: bool = True) -> bool:
    surf.blit(self.title_surf, ((480-self.title_rect[2])/2,(100-self.title_rect[3])/2))
    surf.blit(self.text_surf, ((480-self.text_rect[2])/2,300))
    surf.blit(self.analogtext_surf, (57,235))
    surf.blit(self.arrowtext_surf, (290,235))

    surf.blit(self.cross_surf, (191,292))
    surf.blit(self.arrow_surf, (273,(320-115)/2))
    surf.blit(self.joystick_surf,(70, (320-115)/2))
    return True

class Video:
  def __init__(self, path):
    if not os.path.exists(path):
      raise FileNotFoundError(ENOENT, os.strerror(ENOENT), path)
    set_loglevel("quiet")
        
    self.path = path 
    self.name = os.path.splitext(os.path.basename(path))[0]
    
    self._video = MediaPlayer(path)
    self._frame_num = 0
    
    info = MediaInfo.parse(path).video_tracks[0]
    
    self.frame_rate = float(info.frame_rate)
    self.frame_count = int(info.frame_count)
    self.frame_delay = 1 / self.frame_rate
    self.duration = info.duration / 1000
    self.original_size = (info.width, info.height)
    self.current_size = self.original_size
    
    self.active = True
    self.frame_surf = pygame.Surface((0, 0))
    self.frame_surf.fill(pygame.Color("black"))

    self.alt_resize = pygame.transform.smoothscale

    self.GAME_FONT = pygame.freetype.Font("bin/prstartk.ttf", 13)
    self.title_surf, self.title_rect = self.GAME_FONT.render("VIDEO PLAYER", (255,255,255), (0,0,0), 0, 0, 13)

    self.play_surf, self.play_rect = self.GAME_FONT.render("PLAY", (255,255,255), (0,0,0), 0, 0, 10)
    self.pause_surf, self.pause_rect = self.GAME_FONT.render("PAUSE", (255,255,255), (0,0,0), 0, 0, 10)
    self.replay_surf, self.replay_rect = self.GAME_FONT.render("REPLAY", (255,255,255), (0,0,0), 0, 0, 10)
    self.quit_surf, self.quit_rect = self.GAME_FONT.render("QUIT", (255,255,255), (0,0,0), 0, 0, 10)

    self.circle_surf = pygame.image.load("bin/circle.png").convert()
    self.circle_surf = pygame.transform.scale(self.circle_surf, (23, 23))

    self.cross_surf = pygame.image.load("bin/cross.png").convert()
    self.cross_surf = pygame.transform.scale(self.cross_surf, (23, 23))

    self.triangle_surf = pygame.image.load("bin/triangle.png").convert()
    self.triangle_surf = pygame.transform.scale(self.triangle_surf, (23, 23))

  def close(self):
    self._video.close_player()
    self.frame_surf.fill(pygame.Color("black"))
      
  def restart(self):
    self._video.seek(0, relative=False)
    self._frame_num = 0
    # self.frame_surf = None
    self.active = True
      
  def set_size(self, size: tuple):
    self._video.set_size(*size)
    self.current_size = size

  # volume goes from 0.0 to 1.0
  def set_volume(self, volume: float): 
    self._video.set_volume(volume)
      
  def get_volume(self) -> float:
    return self._video.get_volume()
      
  def get_paused(self) -> bool:
    return self._video.get_pause()
      
  def pause(self):
    self._video.set_pause(True)
      
  def resume(self):
    self._video.set_pause(False)
      
  # gets time in seconds
  def get_pos(self) -> float: 
    return self._video.get_pts()
          
  def toggle_pause(self):
    self._video.toggle_pause()
      
  def _update(self): 
    updated = False
    
    if self._frame_num + 1 == self.frame_count:
      self.active = False 
      return False
    
    while self._video.get_pts() > self._frame_num * self.frame_delay:
      frame = self._video.get_frame()[0]
      self._frame_num += 1
      
      if frame != None:
        size =  frame[0].get_size()
        img = pygame.image.frombuffer(frame[0].to_bytearray()[0], size, "RGB")
        if size != self.current_size:
            img = self.alt_resize(img, self.current_size)
        self.frame_surf = img
        
        updated = True
                
    return updated
  
  # seek uses seconds
  def seek(self, seek_time: int): 
    vid_time = self._video.get_pts()
    if vid_time + seek_time < self.duration and self.active:
      self._video.seek(seek_time)
      while vid_time + seek_time < self._frame_num * self.frame_delay:
          self._frame_num -= 1
      
  def draw(self, surf: pygame.Surface, pos: tuple, force_draw: bool = True) -> bool:
    if self.active and (self._update() or force_draw):
      surf.blit(self.frame_surf, pos)
      surf.blit(self.title_surf, ((480-self.title_rect[2])/2,(50-self.title_rect[3])/2))
      
      surf.blit(self.cross_surf, (60,292))
      surf.fill(pygame.Color("black"), (100, 299, self.pause_rect[2], self.pause_rect[3]))
      if(self.get_paused()):
        surf.blit(self.play_surf, (100, 299))
      else:
        surf.blit(self.pause_surf, (100, 299))

      surf.blit(self.circle_surf, (185,292))
      surf.blit(self.replay_surf, (225, 299))

      surf.blit(self.triangle_surf, (330,292))
      surf.blit(self.quit_surf, (370, 299))

      return True
          
    return False

class Camera(object):
  def __init__(self, device):
    self.cap = aruco(device)
    self.GAME_FONT = pygame.freetype.Font("bin/prstartk.ttf", 13)
    self.text_surf, text_rect = self.GAME_FONT.render("", (255,255,255))
    self.title_surf, self.title_rect = self.GAME_FONT.render("CAMERA VIEW", (255,255,255), (0,0,0), 0, 0, 13)

    self.cross_surf = pygame.image.load("bin/cross.png").convert()
    self.cross_surf = pygame.transform.scale(self.cross_surf, (23, 23))

  def processing(self):
    self.frame, self.ids = self.cap.capture()
    self.frame = np.fliplr(self.frame)
    self.frame = np.rot90(self.frame)
    self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
    self.frame_surf = pygame.surfarray.make_surface(self.frame)

    if(self.ids is not None):
      temp = "IDs : " + str(self.ids[0]) + " detected!"
      self.text_surf, text_rect = self.GAME_FONT.render(temp, (255,255,255), None, 0, 0, 10)
      self.cmd_surf, cmd_rect = self.GAME_FONT.render("Show Video", (255,255,255), (0,0,0), 0, 0, 10)    
        
    elif (isinstance(self.ids, type(None))):
      self.text_surf, text_rect = self.GAME_FONT.render("Searching...", (255,255,255), None, 0, 0, 10)
    
    return self.ids

  def close(self):
    self.cap.destructor()

  def draw(self, surf: pygame.Surface, pos: tuple, force_draw: bool = True) -> bool:
    surf.fill(pygame.Color("black"), (0, 285, 480, 50))
    if(self.ids is not None):
      surf.blit(self.cross_surf, (325,292))
      surf.blit(self.cmd_surf, (365,300))

    surf.blit(self.frame_surf, pos)
    surf.blit(self.title_surf, ((480-self.title_rect[2])/2,(50-self.title_rect[3])/2))
    surf.blit(self.text_surf, (10, 300))
    return True       