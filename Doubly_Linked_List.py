# Linked-list, Ring buffer and heap

'''
Doubly Linked List
Methods inlcuded:
1. append_left()
2. append()
3. insert_before()
4. insert_after()
5. remove()
6. forward_traverse()
7. backward_traverse()
8. pop()
9. pop_left()
10. delete_larger_than_x()
'''

class ListEmptyException(Exception):
    pass

class DataNotFoundException(Exception):
    pass

class DoublyLinkedListNode:
    # Node: the 'unit' of a linked list
    def __init__(self, node_data):
        self.data = node_data  # data
        self.next = None  # reference to the next node
        self.previous = None  # reference to the previous node

class DoublyLinkedList:
    # Linked list class
    def __init__(self):
        self.head = None  # The head will be a Node
        self.tail = None  # The tail will be a Node

    def append(self, node_data):

        node = DoublyLinkedListNode(node_data)

        if not self.head:
            self.head = node
        else:
            self.tail.next = node
            node.previous = self.tail

        self.tail = node

    def append_left(self, node_data):

        node = DoublyLinkedListNode(node_data)

        if not self.head:
            self.append(node_data)
        else:
            self.head.previous = node
            node.next = self.head
        self.head = node

    # 有了双向的reference之后，不管是pop()还是pop_left()都会简化很多
    def pop(self):
        if not self.head:
            raise ListEmptyException('The Linked List is Empty!')

        if self.tail.previous == None:
            return None
        else:
            self.tail = self.tail.previous
            self.tail.next = None

    def pop_left(self):
        if not self.head:
            raise ListEmptyException('The Linked List is Empty!')

        if self.head.next == None:
            return None
        else:
            self.head = self.head.next
            self.head.previous = None


    # 对于 doubly Linked List，在 insert_after/before 之后会比单向链表再多赋值一个previous的索引
    def insert_after(self, target_node_data, new_node_data):

        insert_node = DoublyLinkedListNode(new_node_data)

        if not self.head:
            raise ListEmptyException('The Linked List is Empty!')

        head = self.head
        while head:
            if head.data == target_node_data:
                insert_node.next = head.next
                insert_node.previous = head
                head.next.previous = insert_node
                head.next = insert_node
                if insert_node.next == None:
                    self.tail = insert_node
                return
            head = head.next

        raise DataNotFoundException('The data {0} is not found!'.format(target_node_data))

    def insert_before(self, target_node_data, new_node_data):

        insert_node = DoublyLinkedListNode(new_node_data)

        if not self.head:
            raise ListEmptyException('The Linked List is Empty!')

        if self.head.data == target_node_data:
            return self.append_left(new_node_data)

        head = self.head
        while head:
            if head.data == target_node_data:
                insert_node.previous = head.previous
                insert_node.next = head
                head.previous.next = insert_node
                head.previous = insert_node
                return
            head = head.next

        raise DataNotFoundException('The data {0} is not found!'.format(target_node_data))


    def remove_node(self, x):
        # x is the target data you want to remove

        if not self.head:
            raise ListEmptyException('The Linked List is Empty!')

        # If the head data is the target data
        # simply replace the current head with the next node in the list
        if self.head.data == x:
            self.head = self.head.next
            self.head.previous = None
            return

        # If the target data to be removed is not at the head
        # we start from the head and to iterate through the list
        # 这里我们是正向遍历Linked List删除符合条件的元素的，其实也可以反向遍历
        previous_node = self.head  # shallow copy applied on objects, creating bindings instead of clones
        while previous_node.next:
            if previous_node.next.data == x:
                previous_node.next = previous_node.next.next
                previous_node.next.previous = previous_node
                return
            previous_node = previous_node.next
        raise DataNotFoundException('The data {0} is not found!'.format(x))

    # Utility function
    def forward_traverse(self):
        nodes = []
        nodes.append('None')
        node = self.head
        while node:
            nodes.append(str(node.data))
            node = node.next
        nodes.append('None')
        return '->'.join(nodes)

    def backward_traverse(self):
        nodes = []
        nodes.append('None')
        node = self.tail
        while node:
            nodes.append(str(node.data))
            node = node.previous
        nodes.append('None')
        return '->'.join(nodes)


## This is the basic template of a LinkedList above
## Q1: Iterate the list and delete any node with data value greater than X
def del_lar_x(linked_list, x):
    if not linked_list.head:
        raise ListEmptyException('The given LinkedList is empty!')

    # repeatedly check if the head node's data is greater than x
    while linked_list.head:
        if linked_list.head.data > x:
            linked_list.head = linked_list.head.next
            if not linked_list.head:
                return
            else:
                linked_list.head.previous = None
        else:
            break
        # if not, just break the loop
        # now it's ensured that the head data is no larger than x

    # Now the linked list could be an empty list, just check it before moving on
    previous_node = linked_list.head # shallow copy, shared references
    while previous_node.next:
        if previous_node.next.data <= x:
            previous_node = previous_node.next
        else:
            previous_node.next.previous = None
            previous_node.next = previous_node.next.next
            if previous_node.next == None:
                linked_list.tail = previous_node
                return
            previous_node.next.previous = previous_node
    return


## test code

list_1 = DoublyLinkedList()
list_1.append(1)
list_1.append(2)
list_1.append(3)
list_1.append(4)
list_1.append_left(0)
list_1.append_left(-1)
print(list_1.forward_traverse())
print(list_1.backward_traverse())
'''
Outputs:
None->-1->0->1->2->3->4->None
None->4->3->2->1->0->-1->None
'''

list_1.insert_after(3, 4.5)
list_1.insert_before(2,1.5)
list_1.insert_before(1,0.5)
print(list_1.forward_traverse())
print(list_1.backward_traverse())
'''
Outputs:
None->-1->0->0.5->1->1.5->2->3->4.5->4->None
None->4->4.5->3->2->1.5->1->0.5->0->-1->None
'''

list_1.pop()
list_1.pop_left()
print(list_1.forward_traverse())
print(list_1.backward_traverse())
'''
Outputs:
None->0->0.5->1->1.5->2->3->4.5->None
None->4.5->3->2->1.5->1->0.5->0->None
'''

list_1.remove_node(1)
list_1.remove_node(2)
print(list_1.forward_traverse())
print(list_1.backward_traverse())
'''
Outputs:
None->0->0.5->1.5->3->4.5->None
None->4.5->3->1.5->0.5->0->None
'''

del_lar_x(list_1,2)
print(list_1.forward_traverse())
print(list_1.backward_traverse())
'''
Outputs:
None->0->0.5->1.5->None
None->1.5->0.5->0->None
'''