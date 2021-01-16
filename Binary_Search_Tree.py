'''
Data Structure: Binomial Search Tree
Methods Included:
1. insert()
2. isPresent()
3. minValue()
4. delete()
5. inOrder() / preOrder() / postOrder()
6. isValidBST()
7. BalancedBSTConverter()
'''

class BSTreeNode:
    def __init__(self, node_value):
        self.value = node_value
        self.left = self.right = None

    def __repr__(self):
        return '%d' % self.value


def _insert_node_into_binarysearchtree(root, data):
    if root == None:
        root = BSTreeNode(data)
    # for the first time of insertion, if the root doesn't exist
    # then add the root
    else:
        if (data <= root.value):
            root.left = _insert_node_into_binarysearchtree(root.left, data)
            # going down to the deepest layer where the node doesn't have the left
        else:
            root.right = _insert_node_into_binarysearchtree(root.right, data)
            # going down to the deepest layer where the node doesn't have the right
    return root

def isPresent (root,val):
    # if the value could be found, return 1, else 0

    if not root:
        return False

    if root.value == val:
        return True
    elif root.value>val:
        return isPresent(root.left,val)
    # recurse until the value is found/not found
    else:
        return isPresent(root.right,val)
    # recurse until the value is found/not found

# a utility function to traverse the BST(Left, Root, Right)
def inorder(root):
    if root:
        inorder(root.left)
        print(root.value)
        inorder(root.right)

# a utility function to traverse the BST(Root, Left, Right)
def preorder(root):
    if root:
        print(root.value)
        preorder(root.left)
        preorder(root.right)

# a utility function to traverse the BST(Left, Right, Root)
def postorder(root):
    if root:
        postorder(root.left)
        postorder(root.right)
        print(root.value)

def minValue(root):
    current = root

    while current.left is not None:
        current = current.left
    return current

def delete(root, value):
    if not root:
        return None

    # if the node to be deleted is smaller than the root's value
    # then the node is at the left side at the current root
    # ultimately we need to return an updated left chain of nodes
    if value < root.value:
        root.left = delete(root.left, value)

    # if the node to be deleted is greater than the root's value
    # then the node is at the right side at the current root
    # ultimately we need to return an updated right chain of nodes
    elif value > root.value:
        root.right = delete(root.right, value)

    # after rounds of recursion above
    # the value now is equal to the root's value
    # it's the current root itself to be deleted
    else:

        # 1) for node with only one/zero child node
        # we skip the current node,
        # return the following left/right chain of nodes
        if not root.left:
            temp = root.right
            # root = None
            return temp

        elif not root.right:
            temp = root.left
            # root = None
            return temp

        # 2) for node with both child notes
        # we just find the min value of the right wing
        # and use its value to replace the value of the root
        # without changing the hierarchy between the root and two wings
        # and then delete the min value node at the right wing
        temp = minValue(root.right)
        root.value = temp.value
        root.right = delete(root.right, temp.value)

    return root


# driven code
r = BSTreeNode(50)
r = _insert_node_into_binarysearchtree(r,30)
r = _insert_node_into_binarysearchtree(r,20)
r = _insert_node_into_binarysearchtree(r,40)
r = _insert_node_into_binarysearchtree(r,70)
r = _insert_node_into_binarysearchtree(r, 10)
print('----------in-order Traverse (Left--Root--Right)--------')
inorder(r)
print('----------pre-order Traverse (Root--Left--Right)-------')
preorder(r)
print('----------post-order Traverse (Left--Right--Root)-------')
postorder(r)
print(isPresent(r,80))
print(isPresent(r,40))
delete(r,20)
delete(r,70)
inorder(r)

'''
Leetcode No.98 Binomial Search Tree
The answer is credit to: 
https://leetcode-cn.com/problems/validate-binary-search-tree/
solution/yi-zhang-tu-rang-ni-ming-bai-shang-xia-jie-zui-da-/
'''

def isValidBST(root):  # root is a list of nodes
    return dg(root, -(2 ** 32), 2 ** 32)
    # +- 2**32 are the extreme max/min values here
    # could be replaced by the max/min value of the input

def dg(root, min_v, max_v):
    # root is the current Node

    if root == None:
        # until the root is the end-node, now it has no sub-nodes and returns True
        return True

    if root.val < max_v and root.val > min_v:
        if dg(root.left, min_v, root.val) == False or dg(root.right, root.val, max_v) == False:
            # recurse on the left wing, while updating the max value
            # recurse on the right wing, while updating the min value
            return False
    else:
        return False
    return True

'''
Converting a biased BST into a balanced BST
by GeeksforGeeks reference: 
https://www.geeksforgeeks.org/convert-normal-bst-balanced-bst/?ref=leftbar-rightbar
Input:
          4
        /   \
       3     5
      /       \
     2         6 
    /           \
   1             7
preorder(root-left-right) = 4-3-2-1-5-6-7
Output:
       4
    /    \
   2      6
 /  \    /  \
1    3  5    7 
preorder(root-left-right) = 4-2-1-3-6-5-7
'''
def balanced_tree_converter(root):

    def store_nodes(root, node):
        # node is the list to store all nodes
        # meanwhile, store_nodes will store the nodes in the ascending order
        if not root:
            return None

        store_nodes(root.left, node)
        node.append(root)
        store_nodes(root.right, node)

    def build_tree(nodes, start, end):
        # nodes is a list of nodes
        # start & end are indices
        if start > end:
            return None

        middle = (start+end)//2
        middle_node = nodes[middle]

        # 不断找到位于中间的Node，向左右两边迭代拓展
        # 直到start = middle-1，这时候再次迭代build_tree的时候会返回None
        # 不会继续向下执行代码，即不会再有新的迭代，开始不断返回，最后返回root_middle_node
        middle_node.left = build_tree(nodes,start,middle-1)
        middle_node.right = build_tree(nodes, middle+1, end)
        return middle_node

    node_list = []
    store_nodes(root, node_list)
    length = len(node_list) - 1

    return build_tree(node_list, 0, length)

# Driver Code
unbalanced_tree_node = BSTreeNode(4)
unbalanced_tree_node.left = BSTreeNode(3)
unbalanced_tree_node.left.left = BSTreeNode(2)
unbalanced_tree_node.left.left.left = BSTreeNode(1)
unbalanced_tree_node.right = BSTreeNode(5)
unbalanced_tree_node.right.right = BSTreeNode(6)
unbalanced_tree_node.right.right.right = BSTreeNode(7)

print('The pre-order traverse before balancing')
preorder(unbalanced_tree_node)

new_tree = balanced_tree_converter(unbalanced_tree_node)
print('The pre-order traverse before balancing')
preorder(new_tree)

'''
Converting an ascending Linked List into a Balanced BST
Basically it's to construct the BST from the medium value of LinkedList
and then take the medium value in each sub-intervals until the medium no exist any more
Reference: GeeksforGeeks
https://www.geeksforgeeks.org/sorted-linked-list-to-balanced-bst/?ref=rp
'''
class LinkdeListNode:
    def __init__(self, data):
        self.value = data
        self.next = None

class SinglyLinkedList:
    # Linked list class
    def __init__(self):
        self.head = None
        self.tail = None

    def append_node(self, node_data):
        node = LinkdeListNode(node_data)
        if not self.head:
            self.head = node
        else:
            self.tail.next = node
        self.tail = node

    def node_count(self):
        count = 1
        temp = self.head
        while temp != self.tail:
            temp = temp.next
            count += 1
        return count

    # Utility function
    def __repr__(self):
        nodes = []
        node = self.head
        while node:
            nodes.append(str(node.value))
            node = node.next
        nodes.append('None')
        return '->'.join(nodes)


# Now we build the BST from the Linked List
def BST_builder(linkedlist, count):

    # count is the number of nodes
    if count <= 0:
        return None
    # stop the recursion and return None
    # otherwise continue the recursion

    # The linkedlist is ascending
    # everytime we construct a new root with the current head value
    left = BST_builder(linkedlist, int(count/2))
    root = BSTreeNode(linkedlist.head.value)
    root.left = left
    linkedlist.head = linkedlist.head.next
    # The number of nodes in the right subtree is count-(nodes in the left)-1(root itself)
    # which is count - int(count/2) -1
    root.right = BST_builder(linkedlist, count - int(count/2) -1)

    return root

def converter(linkedlist):

    count = linkedlist.node_count()
    return BST_builder(linkedlist, count)


# driving code
linkedlist_1 = SinglyLinkedList()
for i in range(2,9):
    linkedlist_1.append_node(i)

converted_root = converter(linkedlist_1)
print('------The converted BST from Linked List------')
preorder(converted_root)

'''
Output:
       5
    /     \
   3       7
 /  \     /  \  
2    4   6    8  
preorder(root-left-right) = 5-3-2-4-7-6-8
'''

