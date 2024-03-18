import logic

def main():
    graph = logic.init(get_graph_str())

def get_graph_str():
    f = open("Graph500.txt", "r")
    return f.read()
main()
