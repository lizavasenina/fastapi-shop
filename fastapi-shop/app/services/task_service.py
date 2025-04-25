import copy
from models import Order, OrderItem, Product
from sqlalchemy import select, func, update
from sqlalchemy.orm import Session
from typing import List

W = 1300000

class Object:
    def __init__(self, w, v):
        self.w = w
        self.v = v
    
    def get_weight(self):
        return self.w
    
    def get_value(self):
        return self.v

class Node:
    def __init__(self, obj, bound, parent, isPutted = False, left = None, right = None):
        self.obj = obj
        self.bound = bound
        self.parent = parent
        self.isPutted = isPutted
        self.left = left
        self.right = right

def ratio(obj):
    return obj.get_value() / obj.get_weight()

def bound(obj, next_obj):
    return obj.get_value() + (W - obj.get_weight()) * ratio(next_obj)

def get_tree(objects) -> Node:
    empty = Object(0, 0)
    possible_solutions = []
    best_solution = Node(empty, 0, None)

    objects.sort(key=ratio, reverse=True)
    objects.append(Object(1, 0))

    root = Node(empty, bound(empty, objects[0]), None)
    better_possible_solutions = [(0, root)]
    
    while better_possible_solutions:
        possible_solutions = []
        stack = sorted(better_possible_solutions, key = lambda x: x[1].bound, reverse = True)

        while stack:
            isBetter = True
            current = stack.pop()
            current_node = current[1]
            total = copy.copy(current_node.obj)
            for i in range (current[0], len(objects) - 1):
                current_node.right = Node(copy.copy(current_node.obj), bound(current_node.obj, objects[i + 1]), current_node)
                total.w = current_node.obj.get_weight() + objects[i].get_weight()
                
                if (total.w > W):
                    current_node = current_node.right
                    continue
                
                total.v = current_node.obj.get_value() + objects[i].get_value()
                current_node.left = Node(copy.copy(total), bound(total, objects[i + 1]), current_node, True)

                if max(current_node.left.bound, current_node.right.bound) < best_solution.bound:
                    isBetter = False
                    break

                if current_node.left.bound >= current_node.right.bound:
                    if current_node.right.bound > best_solution.bound:
                        possible_solutions.append((i + 1, current_node.right))
                    current_node = current_node.left
                else:
                    if current_node.left.bound > best_solution.bound:
                        possible_solutions.append((i + 1, current_node.left))
                    current_node = current_node.right
            if isBetter:
                best_solution = current_node
                break
        
        better_possible_solutions = list(filter(lambda x: x[1].bound > best_solution.bound, stack + possible_solutions))
    
    return best_solution

def get_solution(solution, ids) -> List[int]:
    selected_objects = []
    current_node = solution

    for i in range(len(ids), 0, -1):
        if current_node.isPutted:
            selected_objects.append(ids[i - 1])
        current_node = current_node.parent

    return sorted(selected_objects)

def task(db: Session) -> List[int] | dict:
    query = (
        select(
            Order.order_id, 
            Order.priority, 
            func.sum(Product.length * Product.height * Product.width * OrderItem.products_count).label("volume")
            )
            .join(OrderItem, Order.order_id == OrderItem.order_id)
            .join(Product, OrderItem.product_id == Product.product_id)
            .where(Order.status == False)
            .group_by(Order.order_id, Order.priority)
            )
    result = db.execute(query)

    objects = [(row.order_id, row.volume, row.priority) for row in result]
    if not objects: return { "message": "No unfinished orders" }

    objects.sort(key=lambda row: ratio(Object(row[1], row[2])), reverse=True)
    ids = [row[0] for row in objects]
    objects = [Object(row[1], row[2]) for row in objects]

    tree_node = get_tree(objects)
    result = get_solution(tree_node, ids)

    db.execute(update(Order).where(Order.order_id.in_(list(set(ids) - set(result)))).values(priority = Order.priority + 1))
    db.execute(update(Order).where(Order.order_id.in_(result)).values(status=True))

    db.commit()

    return result