from pyformlang.finite_automaton import DeterministicFiniteAutomaton
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton
from pyformlang.finite_automaton import State
from pyformlang.finite_automaton import Symbol

class Deterministic_automata:
	def __init__(self):
		self.trans_list=[]
		# self.transitions = []
		self.dfa = DeterministicFiniteAutomaton()
		
	def add_transition (self,istate,fstate,symb) -> None:
		self.trans_list.append([istate,fstate,symb])
		self.dfa.add_transition(str(istate),str(symb),str(fstate))

	def remove_transition(self,istate,fstate,symb) -> None:
		self.trans_list.remove([istate,fstate,symb])
		self.dfa.remove_transition(str(istate),str(symb),str(fstate))

	def add_start_state(self,state) ->	None:
		self.dfa.add_start_state(str(state))

	def add_final_state(self,state) -> None:
		self.dfa.add_final_state(str(state))

	def get_trans_list(self) -> list:
		return self.trans_list

	def get_final_states(self) -> list:
		return self.dfa.final_states

	def get_start_state(self):	
		return self.dfa.start_state

	def get_transition_table(self) -> dict:
		return self.dfa.to_dict()

	def minimize(self):
		self.dfa = self.dfa.minimize()

	def is_accepts(self,word) -> bool:
		return self.dfa.accepts(word)

	def get_nodes(self):
		return self.dfa.states

	def remove_state(self,state):
		self.dfa._remove_state(str(state))

	def to_regex(self):
		return self.dfa.to_regex()

	def is_dfa(self):
		return self.dfa.is_deterministic()


def transition_input(x):
    x = x.split(',')
    return str(x[0]), str(x[1]), x[2]

class Nondeterministic_automata:
	def __init__(self):
		self.trans_list=[]
		self.nfa = NondeterministicFiniteAutomaton()

	def add_transition (self,istate,fstate,symb) -> None:
		self.trans_list.append([istate,fstate,symb])
		# self.nfa.add_transition(State(istate),Symbol(symb),State(fstate))
		self.nfa.add_transition(istate,symb,fstate)


	def remove_transition(self,istate,fstate,symb) -> None:
		self.trans_list.remove([istate,fstate,symb])
		# self.nfa.remove_transition(State(istate),Symbol(symb),State(fstate))
		self.nfa.remove_transition(istate,symb,fstate)
	
	def add_start_state(self,state) ->	None:
		self.nfa.add_start_state(state)

	def add_final_state(self,state) -> None:
		self.nfa.add_final_state(state)

	def get_trans_list(self) -> list:
		return self.trans_list

	def get_final_states(self) -> list:
		return self.nfa.final_states

	def get_transition_table(self) -> dict:
		return self.nfa.to_dict()

	def minimize(self):
		self.nfa = self.nfa.minimize()

	def is_accepts(self,word) -> bool:
		return self.nfa.accepts(word)

	def get_nodes(self):
		return self.nfa.states

	def remove_state(self,state):
		self.nfa._remove_state(state)

	def get_deterministic_automata(self):
		return self.nfa.to_deterministic()

	def get_deterministic_transitions(self):
		return self.nfa.to_dict()

	def get_deterministic_final_states(self):
		self.nfa.to_deterministic()
		return self.nfa.final_states

	def get_regular_expression(self):
		return self.nfa.to_regex()

	def is_deterministic(self):
		return self.nfa.is_deterministic()

def remove_duplicate_lists(lists):
    # Convert the list of lists to a set of tuple representations of the inner lists
    lists_set = set([tuple(l) for l in lists])
    
    # Convert the set of tuples back to a list of lists
    lists_without_duplicates = [list(l) for l in lists_set]
    
    return lists_without_duplicates