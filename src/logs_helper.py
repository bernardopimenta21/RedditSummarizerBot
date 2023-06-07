# Paths
POSTS_LOG = "./processed_posts.txt"
ERROR_LOG = "./error.log"


def load_log():
    """
    Reads the log file containing processed posts and creates it if it doesn't exist.

    Returns:
    list
        A list of Reddit post IDs that have been processed.
    """

    try:
        with open(POSTS_LOG, "r", encoding="utf-8") as log_file:
            return log_file.read().splitlines()

    except FileNotFoundError:
        with open(POSTS_LOG, "a", encoding="utf-8") as log_file:
            return []


def update_log(post_id):
    """
    Adds the given post ID to the log file containing processed posts.

    Parameters:
    post_id : str
        The ID of a Reddit post to be added to the log.
    """

    with open(POSTS_LOG, "a", encoding="utf-8") as log_file:
        log_file.write("{}\n".format(post_id))


def log_error(error_message):
    """
    Records an error message in the error log file.

    Parameters:
    error_message : str
        A string containing information about the faulty URL and the encountered exception.
    """

    with open(ERROR_LOG, "a", encoding="utf-8") as log_file:
        log_file.write("{}\n".format(error_message))
