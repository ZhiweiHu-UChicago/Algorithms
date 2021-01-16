# Linked-list, Ring buffer and heap

'''
Singly Linked List
Methods include:
1. append_node()
2. pop_node()
3. insert_after()
4. insert_before()
5. remove_node()
6. forward_traverse()
7. remove_node()
8. delete_larger_than_x()
'''

class ListEmptyException(Exception):
    pass
class DataNotFoundException(Exception):
    pass

class SinglyLinkedListNode:
    # Node: the 'unit' of a linked list
    # 节点，即链表的最小单元，包含自身data和指向下一个节点的reference
    def __init__(self, node_data):
        self.data = node_data # data
        self.next = None # reference

class SinglyLinkedList:
    # Linked list class
    def __init__(self):
        self.head = None  # The head will be a Node
        self.tail = None  # The tail will be a Node
        # Remember linked list is a chain of Nodes

    def append_node(self, node_data):

        node = SinglyLinkedListNode(node_data)

        if not self.head:
            self.head = node
            # if the linked list is empty
            # the newly appended node will be the head
        else:
            self.tail.next = node
            # else, append the node to the tail

        self.tail = node
        # Now the newly-appended Node will be the tail

    def pop_node(self):
        if not self.head:
            raise ListEmptyException('The Linked List is Empty!')

        curr_node = self.head
        while curr_node:
            if curr_node.next.next == None:
                self.tail = curr_node
                self.tail.next = None
                return
            curr_node = curr_node.next

    def insert_after(self, target_node_data, new_node_data):
        insert_node = SinglyLinkedListNode(new_node_data)

        if not self.head:
            raise ListEmptyException('The Linked List is Empty!')

        head = self.head
        while head:
            if head.data == target_node_data:
                insert_node.next = head.next
                head.next = insert_node
                if insert_node.next == None:
                    self.tail = insert_node
                return
            head = head.next
        raise DataNotFoundException('The data {0} is not found!'.format(target_node_data))

    def insert_before(self, target_node_data, new_node_data):
        insert_node = SinglyLinkedListNode(new_node_data)

        if not self.head:
            raise ListEmptyException('The Linked List is Empty!')

        # The one difference of insert_before is how it handles the head
        if self.head.data == target_node_data:
            insert_node.next = self.head
            self.head = insert_node
            return

        previous_node = self.head
        while previous_node.next:
            if previous_node.next.data == target_node_data:
                insert_node.next = previous_node.next
                previous_node.next = insert_node
                return
            previous_node = previous_node.next

        raise DataNotFoundException('The data {0} is not found!'.format(target_node_data))


    def remove_node(self, x):
        # x is the target data you want to remove

        if not self.head:
            raise ListEmptyException('The Linked List is Empty!')

        # If the head data is the target data
        # simply replace the current head with the next node in the list
        if self.head.data == x:
            self.head = self.head.next
            return

        # If the target data to be removed is not at the head
        # we start from the head and to iterate through the list
        previous_node = self.head  # shallow copy
        while previous_node.next:
            if previous_node.next.data == x:
                previous_node.next = previous_node.next.next
                return
            previous_node = previous_node.next
        raise DataNotFoundException('The data {0} is not found!'.format(x))

    # Utility function
    def __repr__(self):
        nodes = []
        node = self.head
        while node:
            nodes.append(str(node.data))
            node = node.next
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
        else:
            break
        # if not, just break the loop
        # now it's ensured that the head data is no larger than x

    # Now the linked list could be an empty list, just check it before moving on
    previous_node = linked_list.head
    if not previous_node:
        return

    while previous_node.next:
        if previous_node.next.data <= x:
            previous_node = previous_node.next
        else:
            previous_node.next = previous_node.next.next
    return


## test code

list_1 = SinglyLinkedList()
list_1.append_node(1)
list_1.append_node(2)
list_1.append_node(3)
list_1.append_node(4)
print(list_1)

list_1.insert_after(4, 4.5)
print(list_1)
print(list_1.tail.data)

'''
Outputs:
1->2->3->4->None
1->2->3->4->4.5->None
4.5
'''

list_1.insert_before(2,1.5)
list_1.insert_before(1,0.5)
print(list_1.head.data)
print(list_1)
list_1.pop_node()
print(list_1)
'''
Outputs:
0.5
0.5->1->1.5->2->3->4->4.5->None
0.5->1->1.5->2->3->4->None
'''

list_1.remove_node(1)
list_1.remove_node(4)
print(list_1)

del_lar_x(list_1,5)
print(list_1)
del_lar_x(list_1,2)
print(list_1)

'''
Outputs:
0.5->1.5->2->3->None
0.5->1.5->2->3->None
0.5->1.5->2->None
'''
