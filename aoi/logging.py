import logging

from colorama import init, Fore, Style, Back

init()

colors = {
    "DEBUG": "",
    "INFO": "",
    "WARNING": f"{Fore.YELLOW}{Style.BRIGHT}",
    "ERROR": f"{Fore.LIGHTRED_EX}{Style.BRIGHT}",
    "CRITICAL": f"{Fore.RED}{Style.BRIGHT}",
}
colors2 = {
    "DEBUG": Fore.WHITE,
    "INFO": Fore.BLUE,
    "WARNING": Fore.YELLOW,
    "ERROR": Fore.LIGHTRED_EX,
    "CRITICAL": Fore.RED,
}
styles = {
    "DEBUG": "",
    "INFO": "",
    "WARNING": "",
    "ERROR": "",
    "CRITICAL": Style.BRIGHT,
}
names = {
    "aoi": Fore.BLUE,
    "discord.client": Fore.GREEN,
    "discord.gateway": Fore.MAGENTA
}


class LoggingHandler(logging.StreamHandler):

    def emit(self, record: logging.LogRecord) -> None:
        name = record.name
        level = record.levelno
        level_name = record.levelname
        if name == "aoi":
            split = record.msg.split(":")
            if len(split) == 1:
                sub = None
                message = split[0]
            else:
                sub = split[0]
                message = ":".join(split[1:])
        else:
            message = record.msg
            sub = None

        print(f"{colors2[level_name]}{styles[level_name]}{level_name:>8}{Style.RESET_ALL}"
              f" "
              f"{Style.BRIGHT}{names[name]}{name}{Style.RESET_ALL} " +
              (f"» {Style.BRIGHT}{Fore.LIGHTBLUE_EX}{sub}{Style.RESET_ALL} " if sub else '') +
              f"» "
              f"{colors[level_name]}{message}{Style.RESET_ALL}")