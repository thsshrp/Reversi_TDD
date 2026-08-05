import logging

def get_logger(logfile="game.log"):
    logger = logging.getLogger("ReversiLogger")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.FileHandler(logfile, mode='w', encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

