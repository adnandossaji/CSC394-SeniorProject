'''
WHEN-IF TEAM 4
@Copyright John Pridmore 2017

Prerequisite parsing tree
'''

from enum import Enum
import copy


class node_type(Enum):
    COURSE = 1
    OR     = 2
    AND    = 3
    ERR    = 4

class bool_node(object):
    '''
    node class for boolean expression tree
    '''
    def __init__(self, course="", left=None, right=None, in_node_type="", nested=False):
        self.left = left
        self.right = right
        self.course = course
        if in_node_type == 'or':
            self.n_type = node_type.OR
        elif in_node_type == 'and':
            self.n_type = node_type.AND
        else:
            self.n_type = in_node_type
        self.nested = nested


    def to_n_type(self, type):
        if type == "and":
            self.n_type = node_type.AND
        else:
            self.n_type = node_type.OR

    @classmethod
    def from_str(self, in_str):
        '''
        :param in_str:
        '''
        if in_str == "and":
            return self(node_type=node_type.AND)
        elif in_str == "or":
            return self(node_type=node_type.OR)
        else:
            return self(course=in_str, node_type=node_type.COURSE)

    def __repr__(self):
        return self.course

    def __str__(self):
        return str(self.course)


class bool_tree(object):
    '''
    tree for creating and parsing boolean expression trees
    '''
    def __init__(self, root=None):
        self.root = root
        self.pos = 0


    @classmethod
    def from_node(self, in_root):
        self.root = copy.deepcopy(in_root)
        return self

    # evaluate the tree
    def evaluate(self, taken):
        if self.root and not isinstance(self.root, str):
            bool_left  = self.__evaluate_subtree(self.root.left, taken)
            if self.root.right:
                bool_right = self.__evaluate_subtree(self.root.right, taken)
                if self.root.n_type == node_type.AND:
                    return bool_right and bool_left
                else:
                    return bool_right or bool_left

            elif self.root.left.right:
                bool_right = self.__evaluate_subtree(self.root.left.right, taken)

                if self.root.n_type == node_type.AND:
                    return bool_right and bool_left
                else:
                    return bool_right or bool_left
            
            return bool_left

    def __evaluate_subtree(self, subtree, taken):
            # determine if subtree is a nested expression
            # print(lhs.course)
            if subtree == None:
                return True
            if subtree.n_type == node_type.COURSE:
                return (subtree.course.strip('(').strip(')') in taken)
            elif subtree.n_type == node_type.AND:
                return self.__evaluate_subtree(subtree.right, taken) and self.__evaluate_subtree(subtree.left, taken)
            else:
                return self.__evaluate_subtree(subtree.right, taken) or self.__evaluate_subtree(subtree.left, taken)


    def tree_from_prereq_str(self, prereqs, idx = 0):
        tokenized = prereqs.replace('  and', ' and').split(" ")

        if len(tokenized) == 2:
            return prereqs

        if ' ' in tokenized:
            raise Exception(" tokenizing input string failed because an extra whitespace fucked everything up")

        lhs = None
        rhs = None
        while self.pos < len(tokenized):
            token_str = str(tokenized[self.pos])
            if token_str[-1] == ')': # return for recursive calls on nested expressions
                return lhs
            elif token_str[0] == '(':
                # nested
                if not lhs:
                    self.pos+=2
                    lhs = self.tree_from_prereq_str(" ".join(tokenized), self.pos)
                    lhs.to_n_type(tokenized[self.pos - 2])
                else:
                    # todo
                    self.pos+=2
                    lhs.right = self.tree_from_prereq_str(" ".join(tokenized), self.pos)
            else:
                if not lhs:
                    if (token_str == "or" or token_str == "and"):
                        lhs = bool_node(
                            left=bool_node(
                                course=" ".join([tokenized[self.pos  - 2], tokenized[self.pos - 1]]),
                                in_node_type=node_type.COURSE,
                            ),
                            right=bool_node(
                                course=" ".join([tokenized[self.pos + 1], tokenized[self.pos + 2]]),
                                in_node_type=node_type.COURSE
                            ),
                            in_node_type=tokenized[self.pos]
                        )
                        self.pos += 1

                # if we are still in bounds of the tokenized string
                elif self.pos < len(tokenized):
                    if token_str[0] == '(':
                        rhs = self.to_bool_tree(" ".join(tokenized), self.pos)
                        print(tokenized[self.pos])
                    elif (token_str == "or" or token_str == "and"):
                            # rhs = bool_node()
                            if self.pos >= 2 and self.pos <= len(tokenized) - 2:
                                lhs = bool_node(
                                    left = lhs,
                                    in_node_type=tokenized[self.pos]
                                )
                                print(tokenized[self.pos])
                                if self.pos + 1 < len(tokenized): # and tokenized[self.pos + 1][0] != '(':
                                    lhs.right= bool_node(
                                        course=" ".join([tokenized[self.pos + 1], tokenized[self.pos + 2]]),
                                        in_node_type=node_type.COURSE
                                    )
                                    self.pos += 1
                else:
                    return lhs
            self.pos+=1
        return lhs

    def __str__(self):
        return self.root.course


if __name__ == "__main__":
    test_prereqs = [
        "CSC 301 and CSC 373 and CSC 374",
        "CSC 301 or CSC 383 or CSC 393",
        "CSC 301 or CSC 383 and CSC 374",
        "(CSC 301 or CSC 383 or CSC 393) and CSC 373",
        "(IT 240 or CSC 355)  and (CSC 212 or CSC 242 or CSC 243 or CSC 262 or CSC 224 or CSC 300 or CSC 309)"
    ]
    a, b, c, d = bool_tree(), bool_tree(), bool_tree(), bool_tree()
    a.root  = a.tree_from_prereq_str(test_prereqs[0])
    b.root  = b.tree_from_prereq_str(test_prereqs[1])
    c.root  = c.tree_from_prereq_str(test_prereqs[2])
    d.root  = d.tree_from_prereq_str(test_prereqs[4])
    x = a.evaluate(["CSC 393", "CSC 383", "CSC 301"])
    y = a.evaluate(["CSC 301", "CSC 373", "CSC 374"])
    z = b.evaluate(["CSC 393", "CSC 383", "CSC 301"])
    ai = c.evaluate(["CSC 301", "CSC 374"])
    e = d.evaluate(["IT 240","CSC 355", "(CSC 200"])
    e = d.evaluate(["IT 240","CSC 355", "CSC 212","CSC 242","CSC 243", "CSC 262","CSC 224","CSC 300", "CSC 309"])
    e = d.evaluate(["IT 240","CSC 355"])
    print(x, y, z, ai, e)
