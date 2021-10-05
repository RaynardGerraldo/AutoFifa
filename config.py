import configparser

""" Shortcut config file generator, if not needed do not change """

def confset():
    config = configparser.ConfigParser()

    config['SHRTCUT'] = {}
    config['SHRTCUT']['MINBIN'] = input("Min bin shortcut: ")
    config['SHRTCUT']['MAXBIN'] = input("Max bin shortcut: ")
    config['SHRTCUT']['MINBID'] = input("Min bid shortcut: ")
    config['SHRTCUT']['MAXBID'] = input("Max bid shortcut: ")

    config['SHRTCUT']['SEARCH'] = input("Search shortcut: ")

    config['SHRTCUT']['BUYNOW'] = input("Buy now shortcut: ")
    config['SHRTCUT']['CHOICE'] = input("Would you like to use search + buy now simultaneously? Y or N: ")
    
    if config['SHRTCUT']['CHOICE'] == "":
        config['SHRTCUT']['CHOICE'] = "N"
    with open('shortcut.ini', 'w') as f:
        config.write(f)
