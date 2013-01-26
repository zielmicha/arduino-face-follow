import cv
import serial
import pygame.image

HAAR_CASCADE_PATH = "haarcascade_frontalface_default.xml"
CAMERA_INDEX = 1
def detect_faces(image):
    faces = []
    detected = cv.HaarDetectObjects(image, cascade, storage, 1.2, 2, cv.CV_HAAR_DO_CANNY_PRUNING, (100,100))
    if detected:
        for (x,y,w,h),n in detected:
            faces.append((x,y,w,h))
    return faces

def topg(src):
    src_rgb = cv.CreateMat(src.height, src.width, cv.CV_8UC3)
    cv.CvtColor(src, src_rgb, cv.CV_BGR2RGB)
    return pygame.image.frombuffer(src_rgb.tostring(), cv.GetSize(src_rgb), "RGB")

if __name__ == "__main__":
    surf = pygame.display.set_mode((800, 800))
    cv.NamedWindow("w1", cv.CV_WINDOW_AUTOSIZE)
    s = serial.Serial('/dev/ttyACM1', baudrate=9600)

    capture = cv.CaptureFromCAM(CAMERA_INDEX)
    storage = cv.CreateMemStorage()
    cascade = cv.Load(HAAR_CASCADE_PATH)
    faces = []
    print 'foo'
    i = 0
    last_center = (0,0)
    def delta_to((x, y, w, h)):
        center = (x + w/2, y + h/2)
        return abs(center[0] - last_center[0]) + abs(center[1] - last_center[1])

    while True:
        image = cv.QueryFrame(capture)
        img = image
        timg = cv.CreateImage((img.height,img.width), img.depth, img.channels)
        cv.Transpose(image, timg)
        image = timg

        # Only run the Detection algorithm every 5 frames to improve performance
        if i%5==0:
            faces = detect_faces(image)
            if faces:
                faces.sort(key=delta_to)
                x, y, w, h = faces[0]

                center = (x + w/2, y + h/2)
                exp = (200, 350)
                d = center[0] - exp[0], -(center[1] - exp[1])
                def mkp(v):
                    if abs(v) < 50:
                        return '0'
                    elif v > 0:
                        return '+'
                    else:
                        return '-'
                msg = mkp( d[0] ) + mkp( d[1] )

                print center, msg.strip()
                s.write(msg)
                s.flush()

        for (x,y,w,h) in faces:
            cv.Rectangle(image, (x,y), (x+w,y+h), 255)

        #cv.SaveImage("w%d.png"%i, image)
        surf.blit(topg(image), (0,0))
        pygame.display.flip()
        cv.ShowImage("w1", image)
        i += 1
