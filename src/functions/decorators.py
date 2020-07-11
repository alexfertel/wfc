def log(logger):
    logger.basicConfig(level=logger.INFO)
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger.info(f'Before calling {func.__name__}')
            result = func(*args, **kwargs)
            logger.info(f'After calling {func.__name__}')

            return result
        return wrapper
    return decorator
