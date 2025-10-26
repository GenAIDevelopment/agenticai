from toner import graph, EmailState

def main():
    state = EmailState(
        draft='I will be on leave next week from 26 oct to 2 nov.',
        tone='formal'
    )
    response = graph.invoke(state)
    print(response['mail'])

    


if __name__ == "__main__":
    main()
