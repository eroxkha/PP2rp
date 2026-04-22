import pygame

def rotate_hand(screen, image, center, angle):
    offset = pygame.math.Vector2(0, -image.get_height() // 2)
    offset.rotate_ip(-angle)
    
    rotated_image = pygame.transform.rotate(image, angle)
    rect = rotated_image.get_rect(center=center + offset)
    
    screen.blit(rotated_image, rect)