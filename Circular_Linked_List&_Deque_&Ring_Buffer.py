# Linked-list, Ring buffer and heap

'''
Singly/Doubly Circular Linked List
Methods inlcuded:
1. append()
2. forward_traverse()
3. pop()
'''

class ListEmptyException(Exception):
    pass

class DataNotFoundException(Exception):
    pass

class SinglyCircularLinkedListNode:
    # Node: the 'unit' of a linked list
    # 节点，即链表的最小单元，包含自身data和指向下一个节点的reference
    def __init__(self, node_data):
        self.data = node_data # data
        self.next = None # reference

class SinglyCircularLinkedList:
    # Linked list class
    def __init__(self):
        self.head = None  # The head will be a Node
        self.tail = None  # The tail will be a Node

    def append_node(self, node_data):

        node = SinglyCircularLinkedListNode(node_data)

        if not self.head:
            self.head = node
        else:
            self.tail.next = node
        self.tail = node
        self.tail.next = self.head

    def pop_node(self):
        if not self.head:
            raise ListEmptyException('The Linked List is Empty!')

        curr_node = self.head
        while curr_node:
            if curr_node.next == self.head:
                self.tail = curr_node
                self.tail.next = self.head
                return
            curr_node = curr_node.next

    # Utility function
    def forward_traverse(self):
        nodes = []
        node = self.head
        while node != self.tail:
            nodes.append(str(node.data))
            node = node.next
        nodes.append(str(self.tail.data))
        nodes.append(str(self.head.data))
        return '->'.join(nodes)


## test code

list_1 = SinglyCircularLinkedList()
list_1.append_node(1)
list_1.append_node(2)
list_1.append_node(3)
list_1.append_node(4)
print(list_1.forward_traverse())

list_1.pop_node()
print(list_1.forward_traverse())

'''
Outputs:
1->2->3->4->1
1->2->3->4->1
'''

# deque

from collections import deque
deque_1 = deque()
deque_1.append(3)
deque_1.append(4)

deque_1.appendleft(2)
deque_1.appendleft(1)

deque_1.insert(2, 2.5)
print(deque_1)
'''
Output:
deque([1, 2, 2.5, 3, 4])
'''

deque_1.pop()
deque_1.popleft()
print(deque_1)
'''
Output:
deque([2, 2.5, 3])
'''

deque_1.remove(2.5)
print(deque_1)
'''
Output:
deque([2, 3])
'''

# Circular Buffer
# We use deque() to construct a ring buffer
class FullCircularBufferError(Exception):
    pass

class Ring_Buffer:
    def __init__(self, size, overwrite_mode = True):
        # to switch on/off the overwrite mode
        self.size = size
        self.buffer = deque()
        self.overwrite_mode = overwrite_mode

    def write(self, element):
        if len(self.buffer) >= self.size:
            if self.overwrite_mode == False:
                raise FullCircularBufferError('Buffer Capacity Reached')
            self.buffer.popleft()
        self.buffer.append(element)

    def read(self):
        if len(self.buffer) == 0:
            return None
        return self.buffer.popleft() # remember ring buffer is FIFO

    def __repr__(self):
        result = []
        for elemts in self.buffer:
            result.append(elemts)
        return '['+','.join([str(i) for i in result])+']'

rb_1 = Ring_Buffer(5)
rb_1.write(1)
rb_1.write(2)
rb_1.write(3)
rb_1.write(4)
rb_1.write(5)
rb_1.write(6)
print(rb_1)
# 1 will be dropped to save space for the far-right appended 6

rb_1.read()
rb_1.read()
print(rb_1)
# will output [4,5,6]

rb_2 = Ring_Buffer(2,overwrite_mode=False)
rb_2.write(1)
rb_2.write(2)
rb_2.write(3)
# will report errors