from typing import TypeVar, Generic

T = TypeVar("T")

class Node(Generic[T]):
    def __init__(self, data: T):
        self.__data  = data
        self.__next = None
        self.__prev = None
    
    def set_next(self, next: 'Node[T] | None'):
        self.__next = next

    def set_prev(self, prev: 'Node[T] | None'):
        self.__prev = prev

    def get_next(self):
        return self.__next
    
    def get_prev(self):
        return self.__prev
    
    def get_data(self):
        return self.__data


class Deque(Generic[T]):
    def __init__(self):
        self.__front = None
        self.__back = None
        self.__size = 0


    def front(self):
        if not self.__front:
            raise Exception("front() from empty deque") 
        
        return self.__front.get_data()
    

    def push_front(self, data: T):
        new_node = Node(data)
        self.__size += 1

        if not self.__front:
            self.__front = self.__back = new_node
            return

        new_node.set_prev(self.__front)
        self.__front.set_next(new_node)

        self.__front = new_node

    
    def pop_front(self):
        if self.__front == None:
            raise Exception("pop_front() from empty deque") 
        
        self.__size -= 1
        self.__front = self.__front.get_prev()
        
        if self.__front:
            self.__front.set_next(None)
            return
        
        self.__back = None


    def back(self):
        if not self.__back:
            raise Exception("back() from empty deque") 
        
        return self.__back.get_data()
    

    def push_back(self, data: T):
        new_node = Node(data)
        self.__size += 1

        if not self.__front:
            self.__front = self.__back = new_node
            return

        new_node.set_prev(self.__front)
        self.__front.set_next(new_node)

        self.__front = new_node
    

    def pop_back(self):
        if not self.__back:
            raise Exception("pop_back() from empty deque") 
        
        self.__size -= 1
        self.__back = self.__back.get_next()
        
        if self.__back:
            self.__back.set_prev(None)
            return
        
        self.__front = None


    def __repr__(self):
        print("[", end="")
        for value in self:
            print(value, end=",")
        return "\b]" if self.__front else "]"


    def __iter__(self):
        current_node = self.__front
        while current_node:
            yield current_node.get_data()
            current_node = current_node.get_prev()


    def __len__(self):
        return self.__size