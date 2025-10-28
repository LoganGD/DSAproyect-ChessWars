
class Node:
    def __init__(self, key, data):
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
        self._root = None
        self._size = 0

        if data:
            try:
                for k, d in data:
                    self.add(k,d)
            except:
                self.add(data[0], data[1])

    def add(self,key, data):
        new_node = Node(key, data)
        if self._root:
            self.insert_node(new_node)
            self.__bubble_up(new_node)
        else:
            self._root = new_node
        self._size += 1
        
    def insert_node(self, node: Node):
        path = bin(self._size+1)[3:]
        current = self._root

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
            raise Exception("dequeue from empty queue")

        if self._size == 1:
            self._root =None
        
        node = self.__get_last_node()
        self._root.swap(node)
        self.__remove_last_node()
        self.__bubble_down(self._root)

    def top(self):
        return self._root

    def erase(self, key):
        node = self.__find(self._root, key)
        last_node = self.__get_last_node()
        if node:
            last_node.swap(node)
            self.__remove_last_node()
            self.__bubble_up(node)
            self.__bubble_down(node)

    def change_priority(self, old_key, new_key):
        node = self.__find(self._root, old_key)
        if not node:
            return 
        node.set_key(new_key)

        self.__bubble_up(node)
        self.__bubble_down(node)

    def __find(self,node:Node,key):
        if not node:
            return None
            
        if node.get_key() == key:
            return node
        
        left = self.__find(node.get_left(), key)

        if left:
            return left
        return self.__find(node.get_right(), key)

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
        current = self._root

        for c in path:
            if c=='0':
                current = current.get_left()
            else:
                current = current.get_right()
        
        return current
        
    def __remove_last_node(self):
        if self._size == 1:
            self._root = None
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
        self.__recursive_repr(self._root)
        return ""

if __name__ == "__main__":
    main()