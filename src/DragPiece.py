import pygame

from GlobalConstants import *

class DragPiece:
    def __init__(self):
        self.piece = None
        self.isDragging = False
        self.mouseX = 0
        self.mouseY = 0
        self.initialRow = 0
        self.initialCol = 0

    def updateMouse(self, pos: tuple):
        self.mouseX, self.mouseY = pos

    def saveInitialPos(self, pos):
        self.initialRow = pos[1] // squareSize
        self.initialCol = pos[0] // squareSize

    def startDraggingPiece(self, piece):
        self.piece = piece
        self.isDragging = True

    def stopDraggingPiece(self):
        self.piece = None
        self.isDragging = False

    def updateBlit(self, surface):
        if self.piece != None:
            self.piece.texture_rect.center = self.mouseX, self.mouseY
            surface.blit(Images[self.piece.imageKey], self.piece.texture_rect)
        