





class Crafting:
    def __init__(self, item_matrix):
        self.item_matrix = item_matrix
        
    def craftable(self, proposed):
        for p, a in zip(proposed, self.item_matrix):
            if p is not a:
                return False
        return True
    

                
        
        