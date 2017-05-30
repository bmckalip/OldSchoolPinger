import subprocess
import re
import sys


def ping(server):
    p = subprocess.Popen('ping ' + server, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = ''
    for line in p.stdout:
        output = line.rstrip().decode('UTF-8')
        if output.endswith('unreachable.') or output.startswith('Ping request could not find host') or output.startswith('Request timed out.'):
            # error contacting server
            return [sys.maxsize, sys.maxsize, sys.maxsize]

    # returns the [minimum, maximum, average] ping time as a list
    return [int(x) for x in re.findall(r'\d+', output)]


def findFastestWorld(worlds, printAll=False):
    print("Pinging " + str(len(worlds)) + " servers - this could take several minutes.")

    fastestResult = [-1, [sys.maxsize, sys.maxsize, sys.maxsize]]
    #omission is used to print a new line properly if there was an omission symbol in place of the full result
    omission = False
    for world in worlds:
        hostname = 'oldschool' + str(world) + '.runescape.com'
        speed = ping(hostname)
        currentResult = [world, speed]

        if currentResult[-1][-1] < fastestResult[-1][-1]:
            fastestResult = [world, currentResult[-1]]
            if omission: print()
            print('New fastest world found: ' + str(fastestResult))

        # if the current result's ping differential (max - min) is less than the fastest, update.
        elif currentResult[-1][-1] == fastestResult[-1][-1]:
            if (currentResult[-1][1] - currentResult[-1][0]) < (fastestResult[-1][1] - fastestResult[-1][0]):
                fastestResult = [world, currentResult[-1]]
                if omission: print()
                print('Equally fast, more stable world found: ' + str(fastestResult))

        elif printAll:
            if omission: print()
            print(currentResult)

        else:
            print('.', end='', sep=' ', flush=True)
            omission = True
            continue
        omission = False
    return fastestResult

if __name__ == "__main__":
    notWorlds = [63, 64, 71, 72, 79, 80]
    allWorlds = set(list(range(1, 86)) + [93, 94]) - set(notWorlds)
    freeWorlds = list(range(81, 86)) + [1, 8, 16, 26, 35, 93, 94]
    DMMWorlds = [25, 37, 45]
    worldsToPing = list(set(allWorlds) - set(freeWorlds) - set(DMMWorlds))

    fastestWorld = findFastestWorld(worldsToPing)
    print('\n\nWorld ' + str(fastestWorld[0]) + ' is currently the most stable world with the lowest average ping (of ' + str(fastestWorld[-1][-1]) + ' ms).')
