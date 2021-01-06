from dotenv import load_dotenv
import os
import sys
import logging
import loms

# define main function
def main():
    # load environment variables
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')

    # set up logging
    logging.basicConfig(level=logging.INFO)
    
    # define file names and internal names of reaction dictionaries
    dict_names_list =   ['images', 'images-2', 'special', 'info']
    dict_list = [name + '.json' for name in dict_names_list]

    # instantiate bot
    if len(sys.argv) > 2:
            bot = loms.LOMS(dict_list, dict_names_list, sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2:
            bot = loms.LOMS(dict_list, dict_names_list, sys.argv[1])
    else:
        bot = loms.LOMS(dict_list, dict_names_list)

    # run bot
    bot.run(TOKEN)


# run main()
if __name__ == "__main__":
    main()
