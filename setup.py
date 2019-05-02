import pip
import utilities as utils

DEPENDENCES = ['serial', 'smbus', 'python-qt5', 'pyqtgraph', 'i2c']

def install(package):
    if(hasattr(pip, 'main')):
        pip.main(['install', package])
    elif(hasattr(pip, '__internal')):
        utils.log(0, 'No main class was found when trying to install ' + str(package) + 'switching to internal main.')
        pip.__internal.main(['install', package])

    utils.log(0, str(package) + ' package guaranteed installed.')

def main():
    for i in DEPENDENCES:
        install(i)

if __name__ == '__main__':
    main()
