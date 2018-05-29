# -*- encoding: utf8 -*-
class Elem :
	'''
	Element used in a priority list
	'''
	def __init__(self, prio, thing = None):
		self.prio = prio #The priority value
		self.thing = thing #The thing to store ( task, Object ...)
		
	def __str__(self):
		return '(' + str(self.prio) + ' ; ' +  str (self.thing) + ')'


class SebHeap :
	'''
	The priority list which is in fact a non-binary heap.
	The top element is the one with the lowest priority
	'''
	def __init__(self, head, sub):
		self.head = head #The top element
		self.sub = sub # A list of next heaps with priority higher than head
		
	def __str__(self):
		'''
		The represention with tabulation help to see how the heap is generated.
		'''
		s = ''
		s += '[ ' + str(self.head) + ' children : '
		for i in self.sub :
			s += '\n\t' + str(i) + ','
		s+='\n]'
		return s.replace('\n','\n\t')
	
	def empty(self):
		'''
		Return true if the heap is empty
		'''
		return (self.head is None)

class PrioList :
	'''
	The manager class of the heap
	'''
	def __init__(self, heap = SebHeap(None, [])):
		self.heap = heap #The top heap

	def empty(self):
		'''
		Return true if the heap is empty
		'''
		return (self.heap is None or self.heap.head is None)
	
	def put(self, tuple):
		'''
		Add an element of the format (x,y) with x as the priority value and y the thing to store
		'''
		self.heap = _merge( SebHeap(Elem( tuple[0], tuple[1] ), []), self.heap )
		
	def pop(self):
		'''
		Return the thing stored with the highest priority value
		'''
		self.add=0
		to_ret = self.heap.head.thing
		self.heap = _merge_pairs(self.heap.sub)
		return to_ret
	
	def __str__(self):
		s = '[ ' + str(self.heap) + ' ]'
		return s.replace('\n\t','\n')
#
# More detail in the pdf file
def _merge(prio1, prio2):
	'''
	Complexity of O(1)
	'''
	if prio1.empty():
		return prio2
	elif prio2.empty() :
		return prio1
	elif prio1.head.prio < prio2.head.prio : # Switch for min/max
		prio1.sub.append(prio2) #Complexity of O(1)
		if len(prio1.sub) > 250 :
			prio1.sub = [_merge_pairs(prio1.sub)]
		return SebHeap(prio1.head, prio1.sub) #Complexity of O(1)
	else :
		prio2.sub.append(prio1) #Complexity of O(1)
		if len(prio2.sub) > 250 :
			prio2.sub = [_merge_pairs(prio2.sub)]
		return SebHeap(prio2.head, prio2.sub ) #Complexity of O(1)

def _merge_pairs(db_list):
	if len(db_list) == 0 :
		return SebHeap(None, [])
	elif len(db_list) == 1 :
		return db_list.pop()
	else :
		return _merge( _merge( db_list.pop(), db_list.pop() ) , _merge_pairs(db_list))