from bot.bot import SecuritySystem

import bot.config as config

if __name__ == '__main__':
    security_system = SecuritySystem(token=config.TOKEN)
    security_system.dispatcher.run_polling(security_system)
