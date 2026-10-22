def get_topic(path='./downloads/topic.txt'):
    with open(path, mode='r') as file:
        return file.readlines()[0]


if __name__ == "__main__":
    print(get_topic())