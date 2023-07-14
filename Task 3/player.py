from utils import Player,WINDOW_WIDTH
import cv2
import numpy as np
import keyboard
steps=1
player = Player()
#Initializing a Player object with a random start position on a randomly generated Maze

def display(maze, click, loc):
    maze[maze != 0] = 255
    maze2=maze.copy()
    click[click != 0] = 255
    cv2.namedWindow('snapshot', cv2.WINDOW_NORMAL)
    click[int(click.shape[0] // 2), int(click.shape[1] // 2)]= [0,0,255]
    cv2.imshow('snapshot', click)

    cv2.circle(maze, [int(loc[1] + click.shape[1] // 2), int(loc[0] + click.shape[0] // 2)], 6,
               [0, 0, 255], -1)
    cv2.rectangle(maze, [int(loc[1]), int(loc[0])], [int(loc[1] + click.shape[1]), int(loc[0] + click.shape[0])], [0, 255, 0], 4)

    for i in range(10):
        cv2.imshow('map_identified', maze)
        cv2.waitKey(300)
        cv2.imshow('map_identified', maze2)
        cv2.waitKey(300)
    cv2.imshow('map_identified', maze)
    cv2.waitKey(10)
    cv2.destroyWindow('snapshot')

def strategy():
    map=player.getMap()
    map = map.astype(np.uint8)
    map=cv2.cvtColor(map, cv2.COLOR_GRAY2BGR)


    snapshot=player.getSnapShot()
    snapshot = snapshot.astype(np.uint8)
    snapshot = cv2.cvtColor(snapshot, cv2.COLOR_GRAY2BGR)


    res = cv2.matchTemplate(map, snapshot, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res ==1)

    if len(loc[0])==1:
        print(f'Initial position: {int(loc[0]+snapshot.shape[0]//2)},{int(loc[1]+snapshot.shape[1]//2)}, {len(loc[0])} location matched, accuracy: 1')
        display(map, snapshot, loc)
        movement(loc)
        return 0
    
    #Case if absolute accuracy couldn't get a match
    elif len(loc[0])==0:
        i=1
        while(len(loc[1])==0):
            i-=0.01
            loc = np.where(res >=i)
            if (i<=0): #Running until a match is got
                break



    #Condition if more than same type of environments arise, move randomly and check the surrondings for similarity
    if len(loc[0])>1:
        for pnt in zip(loc[0],loc[1]):
            import random
            h=random.randint(-10,10)
            h_=player.move_horizontal(h)
            v = random.randint(-10, 10)
            v_ = player.move_vertical(v)
            res1 = cv2.matchTemplate(map, snapshot, cv2.TM_SQDIFF)
            loc2 = np.where(res1 >= 0.95)
            if len(loc[0])==1:
                player.move_vertical(-v_)
                player.move_horizontal(-h_)
                print(f'position: {int(loc2[0]-v_ + snapshot.shape[0] // 2)},{int(loc2[1]-h_ + snapshot.shape[1] // 2)} after checking surroundings')

                #return 0
            #return 0

    print(f' Initial position: {int(loc[0] + snapshot.shape[0] // 2)}  {int(loc[1] + snapshot.shape[1] // 2)}, {len(loc[0])} location matched, accuracy: {i}')
    display(map, snapshot, loc)
    movement(loc)

def movement(loc):
    print("You can now control the movements of drone. Try WASD!")
    loc=list(loc)
    while True:
        if keyboard.is_pressed('w'):
            loc[0]+=player.move_vertical(-steps)
        elif keyboard.is_pressed('s'):
            loc[0]+=player.move_vertical(steps)
        elif keyboard.is_pressed('a'):
            loc[1]+=player.move_horizontal(-steps)
        elif keyboard.is_pressed('d'):
            loc[1]+=player.move_horizontal(steps)

        cv2.namedWindow('snapshot', cv2.WINDOW_NORMAL)
        map = player.getMap()
        map = map.astype(np.uint8)
        map = cv2.cvtColor(map, cv2.COLOR_GRAY2BGR)
        map[map!=0]=255
        maze=map
        snapshot = player.getSnapShot()
        snapshot = snapshot.astype(np.uint8)
        snapshot = cv2.cvtColor(snapshot, cv2.COLOR_GRAY2BGR)
        snapshot[snapshot!=0]=255
        click=snapshot

        click[int(click.shape[0] // 2), int(click.shape[1] // 2)] = [0, 0, 255]
        cv2.imshow('snapshot', click)

        cv2.circle(maze, [int(loc[1] + click.shape[1] // 2), int(loc[0] + click.shape[0] // 2)], 6,
                   [0, 0, 255], -1)
        cv2.rectangle(maze, [int(loc[1]), int(loc[0])], [int(loc[1] + click.shape[1]), int(loc[0] + click.shape[0])],
                      [0, 255, 0], 4)

        cv2.imshow('snapshot', snapshot)
        cv2.imshow('map_identified', maze)
        if cv2.waitKey(1) == ord('q'):
            break

if __name__ == "__main__":
    strategy()


#cv2.destroyAllWindows()


























