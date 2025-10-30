
class Node:
    def __init__(self, data, key):
        self.__key = key
        self.__data = data
        self.__left = None
        self.__right = None
        self.__father = None
    
    def swap(self, node: 'Node'):
        node_data = node.get_data()
        node_key = node.get_key()

        node.set_data(self.__data)
        node.set_key(self.__key)

        self.__key, self.__data = node_key, node_data
    
    def get_father(self):
        return self.__father
    
    def get_left(self):
        return self.__left
    
    def get_right(self):
        return self.__right
    
    def get_key(self):
        return self.__key
    
    def get_data(self):
        return self.__data
    
    def set_father(self, node):
        self.__father = node
    
    def set_left(self, node):
        self.__left = node
    
    def set_right(self, node):
        self.__right = node

    def set_key(self, key):
        self.__key = key
    
    def set_data(self, data):
        self.__data = data

class Pqueue:
    def __init__(self, data = None):
        self.__root = None
        self._size = 0

        if data:
            try:
                for d, k in data:
                    self.add(d,k)
            except:
                self.add(data[0], data[1])

    def add(self, data, key):
        new_node = Node( data, key)
        if self.__root:
            self.insert_node(new_node)
            self.__bubble_up(new_node)
        else:
            self.__root = new_node
        self._size += 1
        
    def insert_node(self, node: Node):
        path = bin(self._size+1)[3:]
        current = self.__root

        for c in path:
            parent = current
            if c=='0':
                current = current.get_left()
            else:
                current = current.get_right()
        
        if parent.get_left():
            parent.set_right(node)
        else:
            parent.set_left(node)
        
        node.set_father(parent)

    def pop(self):
        if self._size ==0:
            raise Exception("pop from empty queue")

        if self._size == 1:
            self.__root = None
            return
        
        node = self.__get_last_node()
        self.__root.swap(node)
        self.__remove_last_node()
        self.__bubble_down(self.__root)

    def top(self):
        if self._size ==0:
            raise Exception("top from empty queue")
        return self.__root.get_data()

    def erase(self, data):
        node = self.__find(self.__root, data)
        last_node = self.__get_last_node()
        if node:
            last_node.swap(node)
            self.__remove_last_node()
            self.__bubble_up(node)
            self.__bubble_down(node)

    def change_priority(self, data, new_key, dif=None):
        node = self.__find(self.__root, data)
        if not node:
            return 
        
        if not dif:
            node.set_key(new_key)
        else:
            node.set_key(node.get_key() + dif)

        self.__bubble_up(node)
        self.__bubble_down(node)

    def __find(self,node:Node,data):
        if not node:
            return None
            
        if node.get_data() == data:
            return node
        
        left = self.__find(node.get_left(), data)

        if left:
            return left
        return self.__find(node.get_right(), data)

    def __bubble_up(self, node:Node):
        while node.get_father():
            if node.get_father().get_key() < node.get_key():
                node.swap(node.get_father())
                node = node.get_father()
            else :
                break

    def __bubble_down(self, node:Node):
        while node.get_left():
            bigger_child = node.get_left()

            if node.get_right():
                if node.get_right().get_key() > node.get_left().get_key():
                    bigger_child = node.get_right()
            
            if bigger_child.get_key() > node.get_key():
                node.swap(bigger_child)
                node = bigger_child
            else:
                break

    def __get_last_node(self):
        path = bin(self._size )[3:]
        current = self.__root

        for c in path:
            if c=='0':
                current = current.get_left()
            else:
                current = current.get_right()
        
        return current
        
    def __remove_last_node(self):
        if self._size == 1:
            self.__root = None
            self._size = 0
            return

        node = self.__get_last_node()
        
        if node.get_father().get_right():
            node.get_father().set_right(None)
        else:
            node.get_father().set_left(None)

        self._size -=1

    def __recursive_repr(self, node, deep = 0, st=""):
        if not node:
            return
        if node.get_left():
            self.__recursive_repr(node.get_left(), deep+1, "- ")

        print("  "*deep+ st + f"{node.get_key()}")

        if node.get_right():
            self.__recursive_repr(node.get_right(), deep+1, "- ")

    def __repr__(self):
        self.__recursive_repr(self.__root)
        return ""

def main():
    pass

if __name__ == "__main__":
    main()