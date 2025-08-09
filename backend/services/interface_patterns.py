import pm4py
from pm4py import PetriNet
from pm4py.objects.petri_net.utils import petri_utils

'''
Implementation of all the Interface Patterns described in the underliying paper.
+ IP2b, which is a slight modification of IP2. See for details
'''



class interface_patterns:
	patterns: list = []


	@staticmethod
	def create_ip_1_petri_net():
		# Create a Petri net
		net_ip_1 = PetriNet("IP-1")

		# Add places to the Petri net
		place_A0 = petri_utils.add_place(net_ip_1, 'A0')
		place_A3 = petri_utils.add_place(net_ip_1, 'A3')
		place_A1 = petri_utils.add_place(net_ip_1, 'A1')
		place_a = petri_utils.add_place(net_ip_1, 'a')
		place_A2 = petri_utils.add_place(net_ip_1, 'A2')

		# Add transitions to the Petri net
		transition_a_exclamation = petri_utils.add_transition(net_ip_1, 'a!')
		transition_a_question = petri_utils.add_transition(net_ip_1, 'a?')

		# Create arcs
		petri_utils.add_arc_from_to(place_A0, transition_a_exclamation, net_ip_1)
		petri_utils.add_arc_from_to(place_A3, transition_a_question, net_ip_1)
		petri_utils.add_arc_from_to(transition_a_exclamation, place_a, net_ip_1)
		petri_utils.add_arc_from_to(place_a, transition_a_question, net_ip_1)
		petri_utils.add_arc_from_to(transition_a_question, place_A2, net_ip_1)
		petri_utils.add_arc_from_to(transition_a_exclamation, place_A1, net_ip_1)

		# Define the initial and final marking
		initial_marking = pm4py.objects.petri_net.obj.Marking()
		initial_marking[place_A0] = 1  # Initial token in place A1

		final_marking = pm4py.objects.petri_net.obj.Marking()
		final_marking[place_A3] = 1  # Final token in place A2

		return net_ip_1, initial_marking, final_marking # checked


	@staticmethod
	def create_ip_2_petri_net():
		# Create a Petri net
		net_ip_2 = PetriNet("IP-2")

		# Add places to the Petri net
		place_P0 = petri_utils.add_place(net_ip_2, 'P0')
		place_P1 = petri_utils.add_place(net_ip_2, 'P1')
		place_P2 = petri_utils.add_place(net_ip_2, 'P2')
		place_P3 = petri_utils.add_place(net_ip_2, 'P3')
		place_P4 = petri_utils.add_place(net_ip_2, 'P4')
		place_P5 = petri_utils.add_place(net_ip_2, 'P5')
		place_P6 = petri_utils.add_place(net_ip_2, 'P6')
		place_P7 = petri_utils.add_place(net_ip_2, 'P7')
		place_P8 = petri_utils.add_place(net_ip_2, 'P8')
		place_P9 = petri_utils.add_place(net_ip_2, 'P9')

		place_Pa = petri_utils.add_place(net_ip_2, 'Pa')
		place_Pb = petri_utils.add_place(net_ip_2, 'Pb')


		# Add transitions to the Petri net
		transition_a_exclamation = petri_utils.add_transition(net_ip_2, 'a!')
		transition_a_question = petri_utils.add_transition(net_ip_2, 'a?')
		transition_b_exclamation = petri_utils.add_transition(net_ip_2, 'b!')
		transition_b_question = petri_utils.add_transition(net_ip_2, 'b?')
		transition_c = petri_utils.add_transition(net_ip_2, 'c')
		transition_d = petri_utils.add_transition(net_ip_2, 'd')



		# Create arcs
		# left side
		petri_utils.add_arc_from_to(place_P0, transition_c,
		                            net_ip_2)
		petri_utils.add_arc_from_to(transition_c, place_P1, net_ip_2)
		petri_utils.add_arc_from_to(transition_c, place_P2, net_ip_2)
		petri_utils.add_arc_from_to(place_P1, transition_a_exclamation, net_ip_2)

		petri_utils.add_arc_from_to(place_P2, transition_b_exclamation,
		                            net_ip_2)
		petri_utils.add_arc_from_to(transition_a_exclamation, place_P3,
		                            net_ip_2)
		petri_utils.add_arc_from_to(transition_b_exclamation, place_P4, net_ip_2)

		# right side
		petri_utils.add_arc_from_to(place_P5, transition_d, net_ip_2)

		petri_utils.add_arc_from_to(transition_d, place_P6,
		                            net_ip_2)
		petri_utils.add_arc_from_to(transition_d, place_P7,
		                            net_ip_2)
		petri_utils.add_arc_from_to(place_P6, transition_b_question, net_ip_2)
		petri_utils.add_arc_from_to(place_P7, transition_a_question, net_ip_2)

		petri_utils.add_arc_from_to(transition_b_question, place_P8, net_ip_2)
		petri_utils.add_arc_from_to(transition_a_question, place_P9, net_ip_2)

		# interactions:
		petri_utils.add_arc_from_to(transition_a_exclamation, place_Pa, net_ip_2)
		petri_utils.add_arc_from_to(place_Pa, transition_a_question, net_ip_2)

		petri_utils.add_arc_from_to(transition_b_exclamation, place_Pb, net_ip_2)
		petri_utils.add_arc_from_to(place_Pb, transition_b_question, net_ip_2)


	# Define the initial and final marking
		initial_marking = pm4py.objects.petri_net.obj.Marking()
		initial_marking[place_P1] = 1  # Initial token in place A1

		final_marking = pm4py.objects.petri_net.obj.Marking()
		final_marking[place_P5] = 1  # Final token in place A2

		return net_ip_2, initial_marking, final_marking




	@staticmethod
	def create_ip_2b_petri_net():
		"""
		Slight variation of the ip_2 net that uses 2 transitions to merge the 4 final places into 2
		"""
		# Create a Petri net
		net_ip_2 = PetriNet("IP-2b")

		# Add places to the Petri net
		place_P0 = petri_utils.add_place(net_ip_2, 'P0')
		place_P1 = petri_utils.add_place(net_ip_2, 'P1')
		place_P2 = petri_utils.add_place(net_ip_2, 'P2')
		place_P3 = petri_utils.add_place(net_ip_2, 'P3')
		place_P4 = petri_utils.add_place(net_ip_2, 'P4')
		place_P5 = petri_utils.add_place(net_ip_2, 'P5')
		place_P6 = petri_utils.add_place(net_ip_2, 'P6')
		place_P7 = petri_utils.add_place(net_ip_2, 'P7')
		place_P8 = petri_utils.add_place(net_ip_2, 'P8')
		place_P9 = petri_utils.add_place(net_ip_2, 'P9')

		place_Pa = petri_utils.add_place(net_ip_2, 'Pa')
		place_Pb = petri_utils.add_place(net_ip_2, 'Pb')

		place_P10 = petri_utils.add_place(net_ip_2, 'P10')
		place_P11 = petri_utils.add_place(net_ip_2, 'P11')
		# Add transitions to the Petri net
		transition_a_exclamation = petri_utils.add_transition(net_ip_2, 'a!')
		transition_a_question = petri_utils.add_transition(net_ip_2, 'a?')
		transition_b_exclamation = petri_utils.add_transition(net_ip_2, 'b!')
		transition_b_question = petri_utils.add_transition(net_ip_2, 'b?')
		transition_c = petri_utils.add_transition(net_ip_2, 'c')
		transition_d = petri_utils.add_transition(net_ip_2, 'd')

		transition_e = petri_utils.add_transition(net_ip_2, 'e')
		transition_f = petri_utils.add_transition(net_ip_2, 'f')

		# Create arcs
		# left side
		petri_utils.add_arc_from_to(place_P0, transition_c,
		                            net_ip_2)
		petri_utils.add_arc_from_to(transition_c, place_P1, net_ip_2)
		petri_utils.add_arc_from_to(transition_c, place_P2, net_ip_2)
		petri_utils.add_arc_from_to(place_P1, transition_a_exclamation, net_ip_2)

		petri_utils.add_arc_from_to(place_P2, transition_b_exclamation,
		                            net_ip_2)
		petri_utils.add_arc_from_to(transition_a_exclamation, place_P3,
		                            net_ip_2)
		petri_utils.add_arc_from_to(transition_b_exclamation, place_P4, net_ip_2)

		# right side
		petri_utils.add_arc_from_to(place_P5, transition_d, net_ip_2)

		petri_utils.add_arc_from_to(transition_d, place_P6,
		                            net_ip_2)
		petri_utils.add_arc_from_to(transition_d, place_P7,
		                            net_ip_2)
		petri_utils.add_arc_from_to(place_P6, transition_b_question, net_ip_2)
		petri_utils.add_arc_from_to(place_P7, transition_a_question, net_ip_2)

		petri_utils.add_arc_from_to(transition_b_question, place_P8, net_ip_2)
		petri_utils.add_arc_from_to(transition_a_question, place_P9, net_ip_2)

		# interactions:
		petri_utils.add_arc_from_to(transition_a_exclamation, place_Pa, net_ip_2)
		petri_utils.add_arc_from_to(place_Pa, transition_a_question, net_ip_2)

		petri_utils.add_arc_from_to(transition_b_exclamation, place_Pb, net_ip_2)
		petri_utils.add_arc_from_to(place_Pb, transition_b_question, net_ip_2)

		petri_utils.add_arc_from_to(place_P4, transition_e, net_ip_2)
		petri_utils.add_arc_from_to(place_P3, transition_e, net_ip_2)
		petri_utils.add_arc_from_to(place_P8, transition_f, net_ip_2)
		petri_utils.add_arc_from_to(place_P9, transition_f, net_ip_2)

		petri_utils.add_arc_from_to(transition_e, place_P10, net_ip_2)
		petri_utils.add_arc_from_to(transition_f, place_P11, net_ip_2)

	# Define the initial and final marking
		initial_marking = pm4py.objects.petri_net.obj.Marking()
		initial_marking[place_P1] = 1  # Initial token in place A1

		final_marking = pm4py.objects.petri_net.obj.Marking()
		final_marking[place_P5] = 1  # Final token in place A2

		return net_ip_2, initial_marking, final_marking

	@staticmethod
	def create_ip_3_petri_net():
		# Create a Petri net
		net_ip_3 = PetriNet("IP-3")

		# Add places to the Petri net
		place_0 = petri_utils.add_place(net_ip_3, '0')
		place_1 = petri_utils.add_place(net_ip_3, '1')
		place_a = petri_utils.add_place(net_ip_3, 'a')
		place_b = petri_utils.add_place(net_ip_3, 'b')
		place_A1 = petri_utils.add_place(net_ip_3, 'A1')
		place_A2 = petri_utils.add_place(net_ip_3, 'A2')

		# Add transitions to the Petri net
		transition_a_exclamation = petri_utils.add_transition(net_ip_3, 'a!')
		transition_a_question = petri_utils.add_transition(net_ip_3, 'a?')
		transition_b_exclamation = petri_utils.add_transition(net_ip_3, 'b!')
		transition_b_question = petri_utils.add_transition(net_ip_3, 'b?')

		# Create arcs
		petri_utils.add_arc_from_to(place_0, transition_a_exclamation, net_ip_3)
		petri_utils.add_arc_from_to(place_0, transition_b_exclamation, net_ip_3)
		petri_utils.add_arc_from_to(place_1, transition_b_question, net_ip_3)
		petri_utils.add_arc_from_to(place_1, transition_a_question, net_ip_3)

		petri_utils.add_arc_from_to(transition_a_exclamation, place_A1, net_ip_3)
		petri_utils.add_arc_from_to(transition_b_exclamation, place_A1, net_ip_3)
		petri_utils.add_arc_from_to(transition_a_question, place_A2, net_ip_3)
		petri_utils.add_arc_from_to(transition_b_question, place_A2, net_ip_3)

		petri_utils.add_arc_from_to(transition_a_exclamation, place_a, net_ip_3)
		petri_utils.add_arc_from_to(place_a, transition_a_question, net_ip_3)

		petri_utils.add_arc_from_to(transition_b_exclamation, place_b, net_ip_3)
		petri_utils.add_arc_from_to(place_b, transition_b_question, net_ip_3)



		# Define the initial and final marking
		initial_marking = pm4py.objects.petri_net.obj.Marking()
		initial_marking[place_0] = 1

		final_marking = pm4py.objects.petri_net.obj.Marking()
		final_marking[place_1] = 1

		return net_ip_3, initial_marking, final_marking

	@staticmethod
	def create_ip_4_petri_net():
		# Create a Petri net
		net_ip_4 = PetriNet("IP-4")

		# Add places to the Petri net
		place_A1 = petri_utils.add_place(net_ip_4, 'A1')
		place_A2 = petri_utils.add_place(net_ip_4, 'A2')
		place_a = petri_utils.add_place(net_ip_4, 'a')
		place_b = petri_utils.add_place(net_ip_4, 'b')
		place_1 = petri_utils.add_place(net_ip_4, 'P1')
		place_2 = petri_utils.add_place(net_ip_4, 'P2')
		place_3 = petri_utils.add_place(net_ip_4, 'P3')
		place_4 = petri_utils.add_place(net_ip_4, 'P4')

		# Add transitions to the Petri net
		transition_a_exclamation = petri_utils.add_transition(net_ip_4, 'a!')
		transition_a_question = petri_utils.add_transition(net_ip_4, 'a?')
		transition_b_exclamation = petri_utils.add_transition(net_ip_4, 'b!')
		transition_b_question = petri_utils.add_transition(net_ip_4, 'b?')


		# Create arcs
		petri_utils.add_arc_from_to(place_1, transition_a_exclamation, net_ip_4)
		petri_utils.add_arc_from_to(transition_a_exclamation, place_2, net_ip_4)
		petri_utils.add_arc_from_to(place_2, transition_b_question, net_ip_4)
		petri_utils.add_arc_from_to(transition_b_question, place_A1, net_ip_4)

		petri_utils.add_arc_from_to(place_3, transition_a_question, net_ip_4)
		petri_utils.add_arc_from_to(transition_a_question, place_4, net_ip_4)
		petri_utils.add_arc_from_to(place_4, transition_b_exclamation, net_ip_4)
		petri_utils.add_arc_from_to(transition_b_exclamation, place_A2, net_ip_4)

		petri_utils.add_arc_from_to(transition_a_exclamation, place_a, net_ip_4)
		petri_utils.add_arc_from_to(place_a, transition_a_question, net_ip_4)

		petri_utils.add_arc_from_to(transition_b_exclamation, place_b, net_ip_4)
		petri_utils.add_arc_from_to(place_b, transition_b_question, net_ip_4)

		# Define the initial and final marking
		initial_marking = pm4py.objects.petri_net.obj.Marking()
		initial_marking[place_A1] = 1  # Initial token in place A1

		final_marking = pm4py.objects.petri_net.obj.Marking()
		final_marking[place_A2] = 1  # Final token in place A2

		return net_ip_4, initial_marking, final_marking

	@staticmethod
	def create_ip_5_petri_net():
		# Create a Petri net
		net_ip_5 = PetriNet("IP-5")

		# Add places to the Petri net
		place_P0 = petri_utils.add_place(net_ip_5, 'P0')
		place_P1 = petri_utils.add_place(net_ip_5, 'P1')
		place_P2 = petri_utils.add_place(net_ip_5, 'P2')
		place_P3 = petri_utils.add_place(net_ip_5, 'P3')
		place_P4 = petri_utils.add_place(net_ip_5, 'P4')
		place_P5 = petri_utils.add_place(net_ip_5, 'P5')
		place_P6 = petri_utils.add_place(net_ip_5, 'P6')
		place_P7 = petri_utils.add_place(net_ip_5, 'P7')
		place_P8 = petri_utils.add_place(net_ip_5, 'P8')
		place_P9 = petri_utils.add_place(net_ip_5, 'P9')


		place_PA1_1 = petri_utils.add_place(net_ip_5, 'PA1_1')
		place_PA1_2 = petri_utils.add_place(net_ip_5, 'PA1_2')
		place_PA2_1 = petri_utils.add_place(net_ip_5, 'PA2_1')
		place_PA2_2 = petri_utils.add_place(net_ip_5, 'PA2_2')

		place_Pa = petri_utils.add_place(net_ip_5, 'Pa')
		place_Pb = petri_utils.add_place(net_ip_5, 'Pb')
		place_Pc = petri_utils.add_place(net_ip_5, 'Pc')
		place_Pd = petri_utils.add_place(net_ip_5, 'Pd')

		# Add transitions to the Petri net

		t1 = petri_utils.add_transition(net_ip_5, 't1')
		t2 = petri_utils.add_transition(net_ip_5, 't2')

		transition_a_exclamation = petri_utils.add_transition(net_ip_5, 'a!')
		transition_a_question = petri_utils.add_transition(net_ip_5, 'a?')
		transition_b_exclamation = petri_utils.add_transition(net_ip_5, 'b!')
		transition_b_question = petri_utils.add_transition(net_ip_5, 'b?')
		transition_c_exclamation = petri_utils.add_transition(net_ip_5, 'c!')
		transition_c_question = petri_utils.add_transition(net_ip_5, 'c?')
		transition_d_exclamation = petri_utils.add_transition(net_ip_5, 'd!')
		transition_d_question = petri_utils.add_transition(net_ip_5, 'd?')

		# Create arcs
		# left side
		petri_utils.add_arc_from_to(place_P0, t1, net_ip_5)
		petri_utils.add_arc_from_to(t1, place_P1, net_ip_5)
		petri_utils.add_arc_from_to(t1, place_P2, net_ip_5)

		petri_utils.add_arc_from_to(place_P1, transition_a_exclamation, net_ip_5)
		petri_utils.add_arc_from_to(place_P2, transition_b_exclamation, net_ip_5)
		petri_utils.add_arc_from_to(transition_a_exclamation, place_P3, net_ip_5)
		petri_utils.add_arc_from_to(transition_b_exclamation, place_P4, net_ip_5)
		petri_utils.add_arc_from_to(place_P3, transition_c_question, net_ip_5)
		petri_utils.add_arc_from_to(place_P4, transition_d_question, net_ip_5)
		petri_utils.add_arc_from_to(transition_c_question, place_PA1_1, net_ip_5)
		petri_utils.add_arc_from_to(transition_d_question, place_PA1_2, net_ip_5)

		# right side
		petri_utils.add_arc_from_to(place_P5, t2, net_ip_5)
		petri_utils.add_arc_from_to(t2, place_P6, net_ip_5)
		petri_utils.add_arc_from_to(t2, place_P7, net_ip_5)

		petri_utils.add_arc_from_to(place_P7, transition_a_question, net_ip_5)
		petri_utils.add_arc_from_to(place_P6, transition_b_question, net_ip_5)

		petri_utils.add_arc_from_to(transition_b_question, place_P8, net_ip_5)
		petri_utils.add_arc_from_to(transition_a_question, place_P9, net_ip_5)
		petri_utils.add_arc_from_to(place_P8, transition_d_exclamation, net_ip_5)
		petri_utils.add_arc_from_to(place_P9, transition_c_exclamation, net_ip_5)
		petri_utils.add_arc_from_to(transition_d_exclamation, place_PA2_1, net_ip_5)
		petri_utils.add_arc_from_to(transition_c_exclamation, place_PA2_2, net_ip_5)

		# interactions:
		petri_utils.add_arc_from_to(transition_a_exclamation, place_Pa, net_ip_5)
		petri_utils.add_arc_from_to(place_Pa, transition_a_question, net_ip_5)

		petri_utils.add_arc_from_to(transition_b_exclamation, place_Pb, net_ip_5)
		petri_utils.add_arc_from_to(place_Pb, transition_b_question, net_ip_5)

		petri_utils.add_arc_from_to(transition_c_exclamation, place_Pc, net_ip_5)
		petri_utils.add_arc_from_to(place_Pc, transition_c_question, net_ip_5)

		petri_utils.add_arc_from_to(transition_d_exclamation, place_Pd, net_ip_5)
		petri_utils.add_arc_from_to(place_Pd, transition_d_question, net_ip_5)

		# Define the initial and final marking
		initial_marking = pm4py.objects.petri_net.obj.Marking()
		initial_marking[place_P0] = 1  # Initial token in place P0

		final_marking = pm4py.objects.petri_net.obj.Marking()
		final_marking[place_P5] = 1  # Final token in place P5

		return net_ip_5, initial_marking, final_marking

	@staticmethod
	def create_ip_6_petri_net():
		# Create a Petri net
		net_ip_6 = PetriNet("IP-6")

		# Add places to the Petri net
		place_1 = petri_utils.add_place(net_ip_6, 'P1')
		place_2 = petri_utils.add_place(net_ip_6, 'P2')
		place_3 = petri_utils.add_place(net_ip_6, 'P3')
		place_4 = petri_utils.add_place(net_ip_6, 'P4')
		place_5 = petri_utils.add_place(net_ip_6, 'P5')
		place_6 = petri_utils.add_place(net_ip_6, 'P6')

		place_a = petri_utils.add_place(net_ip_6, 'Pa')
		place_b = petri_utils.add_place(net_ip_6, 'Pb')
		place_c = petri_utils.add_place(net_ip_6, 'Pc')
		place_d = petri_utils.add_place(net_ip_6, 'Pd')

		place_A1 = petri_utils.add_place(net_ip_6, 'PA1')
		place_A2 = petri_utils.add_place(net_ip_6, 'PA2')


		# Add transitions to the Petri net
		transition_a_exclamation = petri_utils.add_transition(net_ip_6, 'a!')
		transition_a_question = petri_utils.add_transition(net_ip_6, 'a?')
		transition_b_exclamation = petri_utils.add_transition(net_ip_6, 'b!')
		transition_b_question = petri_utils.add_transition(net_ip_6, 'b?')
		transition_c_exclamation = petri_utils.add_transition(net_ip_6, 'c!')
		transition_c_question = petri_utils.add_transition(net_ip_6, 'c?')
		transition_d_exclamation = petri_utils.add_transition(net_ip_6, 'd!')
		transition_d_question = petri_utils.add_transition(net_ip_6, 'd?')


		# Create arcs
		petri_utils.add_arc_from_to(place_1, transition_a_exclamation, net_ip_6)
		petri_utils.add_arc_from_to(place_1, transition_b_exclamation, net_ip_6)
		petri_utils.add_arc_from_to(transition_a_exclamation, place_2, net_ip_6)
		petri_utils.add_arc_from_to(transition_b_exclamation, place_3, net_ip_6)

		petri_utils.add_arc_from_to(place_2, transition_c_question, net_ip_6)
		petri_utils.add_arc_from_to(place_3, transition_d_question, net_ip_6)
		petri_utils.add_arc_from_to(transition_c_question, place_A1, net_ip_6)
		petri_utils.add_arc_from_to(transition_d_question, place_A1, net_ip_6)

		petri_utils.add_arc_from_to(place_4, transition_a_question, net_ip_6)
		petri_utils.add_arc_from_to(place_4, transition_b_question, net_ip_6)
		petri_utils.add_arc_from_to(transition_a_question, place_5, net_ip_6)
		petri_utils.add_arc_from_to(transition_b_question, place_6, net_ip_6)

		petri_utils.add_arc_from_to(place_5, transition_c_exclamation, net_ip_6)
		petri_utils.add_arc_from_to(place_6, transition_d_exclamation, net_ip_6)
		petri_utils.add_arc_from_to(transition_c_exclamation, place_A2, net_ip_6)
		petri_utils.add_arc_from_to(transition_d_exclamation, place_A2, net_ip_6)

		# interaction arcs
		petri_utils.add_arc_from_to(transition_a_exclamation, place_a, net_ip_6)
		petri_utils.add_arc_from_to(place_a, transition_a_question, net_ip_6)

		petri_utils.add_arc_from_to(transition_b_exclamation, place_b, net_ip_6)
		petri_utils.add_arc_from_to(place_b, transition_b_question, net_ip_6)

		petri_utils.add_arc_from_to(transition_c_exclamation, place_c, net_ip_6)
		petri_utils.add_arc_from_to(place_c, transition_c_question, net_ip_6)

		petri_utils.add_arc_from_to(transition_d_exclamation, place_d, net_ip_6)
		petri_utils.add_arc_from_to(place_d, transition_d_question, net_ip_6)


		# Define the initial and final marking
		initial_marking = pm4py.objects.petri_net.obj.Marking()
		initial_marking[place_1] = 1  # Initial token in place A1

		final_marking = pm4py.objects.petri_net.obj.Marking()
		final_marking[place_4] = 1  # Final token in place A2

		return net_ip_6, initial_marking, final_marking


	@staticmethod
	def create_ip_7_petri_net():
		# Create a Petri net
		net_ip_7 = PetriNet("IP-7")

		# Add places to the Petri net
		place_A1 = petri_utils.add_place(net_ip_7, 'A1')
		place_A2 = petri_utils.add_place(net_ip_7, 'A2')

		place_1 = petri_utils.add_place(net_ip_7, 'P1')
		place_2 = petri_utils.add_place(net_ip_7, 'P2')
		place_3 = petri_utils.add_place(net_ip_7, 'P3')
		place_4 = petri_utils.add_place(net_ip_7, 'P4')
		place_5 = petri_utils.add_place(net_ip_7, 'P5')
		place_6 = petri_utils.add_place(net_ip_7, 'P6')

		place_a = petri_utils.add_place(net_ip_7, 'Pa')
		place_b = petri_utils.add_place(net_ip_7, 'Pb')
		place_c = petri_utils.add_place(net_ip_7, 'Pc')

		# Add transitions to the Petri net
		transition_a_exclamation = petri_utils.add_transition(net_ip_7, 'a!')
		transition_a_question = petri_utils.add_transition(net_ip_7, 'a?')
		transition_b_exclamation = petri_utils.add_transition(net_ip_7, 'b!')
		transition_b_question = petri_utils.add_transition(net_ip_7, 'b?')
		transition_c_exclamation = petri_utils.add_transition(net_ip_7, 'c!')
		transition_c_question = petri_utils.add_transition(net_ip_7, 'c?')

		t1 = petri_utils.add_transition(net_ip_7, 't1')
		t2 = petri_utils.add_transition(net_ip_7, 't2')

		# Create arcs

		petri_utils.add_arc_from_to(place_1, t1, net_ip_7)
		petri_utils.add_arc_from_to(t1, place_2, net_ip_7)
		petri_utils.add_arc_from_to(place_2, transition_c_exclamation, net_ip_7)
		petri_utils.add_arc_from_to(transition_c_exclamation, place_A1, net_ip_7)

		petri_utils.add_arc_from_to(place_2, transition_b_exclamation, net_ip_7)
		petri_utils.add_arc_from_to(transition_b_exclamation, place_3, net_ip_7)
		petri_utils.add_arc_from_to(place_3, transition_a_question, net_ip_7)
		petri_utils.add_arc_from_to(transition_a_question, place_2, net_ip_7)

		petri_utils.add_arc_from_to(place_4, t2, net_ip_7)
		petri_utils.add_arc_from_to(t2, place_5, net_ip_7)
		petri_utils.add_arc_from_to(place_5, transition_c_question, net_ip_7)
		petri_utils.add_arc_from_to(transition_c_question, place_A2, net_ip_7)

		petri_utils.add_arc_from_to(place_5, transition_a_exclamation, net_ip_7)
		petri_utils.add_arc_from_to(transition_a_exclamation, place_6, net_ip_7)
		petri_utils.add_arc_from_to(place_6, transition_b_question, net_ip_7)
		petri_utils.add_arc_from_to(transition_b_question, place_5, net_ip_7)



		# interaction arcs:
		petri_utils.add_arc_from_to(transition_a_exclamation, place_a, net_ip_7)
		petri_utils.add_arc_from_to(place_a, transition_a_question, net_ip_7)

		petri_utils.add_arc_from_to(transition_b_exclamation, place_b, net_ip_7)
		petri_utils.add_arc_from_to(place_b, transition_b_question, net_ip_7)

		petri_utils.add_arc_from_to(transition_c_exclamation, place_c, net_ip_7)
		petri_utils.add_arc_from_to(place_c, transition_c_question, net_ip_7)

		# Define the initial and final marking
		initial_marking = pm4py.objects.petri_net.obj.Marking()
		initial_marking[place_A1] = 1  # Initial token in place A1

		final_marking = pm4py.objects.petri_net.obj.Marking()
		final_marking[place_A2] = 1  # Final token in place A2

		return net_ip_7, initial_marking, final_marking

	@staticmethod
	def create_ip_8_petri_net():
		# Create a Petri net
		net_ip_8 = PetriNet("IP-8")

		# Add places to the Petri net
		place_1 = petri_utils.add_place(net_ip_8, 'P1')
		place_2 = petri_utils.add_place(net_ip_8, 'P2')
		place_3 = petri_utils.add_place(net_ip_8, 'P3')
		place_4 = petri_utils.add_place(net_ip_8, 'P4')
		place_5 = petri_utils.add_place(net_ip_8, 'P5')
		place_6 = petri_utils.add_place(net_ip_8, 'P6')
		place_7 = petri_utils.add_place(net_ip_8, 'P7')
		place_8 = petri_utils.add_place(net_ip_8, 'P8')
		place_9 = petri_utils.add_place(net_ip_8, 'P9')
		place_10 = petri_utils.add_place(net_ip_8, 'P10')
		place_11 = petri_utils.add_place(net_ip_8, 'P11')
		place_12 = petri_utils.add_place(net_ip_8, 'P12')
		place_13 = petri_utils.add_place(net_ip_8, 'P13')
		place_14 = petri_utils.add_place(net_ip_8, 'P14')
		place_15 = petri_utils.add_place(net_ip_8, 'P15')

		place_A1 = petri_utils.add_place(net_ip_8, 'A1')
		place_A2 = petri_utils.add_place(net_ip_8, 'A2')
		place_A3 = petri_utils.add_place(net_ip_8, 'A3')

		place_ackA = petri_utils.add_place(net_ip_8, 'ackA')
		place_ackB = petri_utils.add_place(net_ip_8, 'ackB')
		place_aR = petri_utils.add_place(net_ip_8, 'aR')
		place_bR = petri_utils.add_place(net_ip_8, 'bR')
		place_a = petri_utils.add_place(net_ip_8, 'Pa')
		place_b = petri_utils.add_place(net_ip_8, 'Pb')

		# Add transitions to the Petri net
		transition_a_exclamation = petri_utils.add_transition(net_ip_8, 'a!')
		transition_a_question_1 = petri_utils.add_transition(net_ip_8, 'a?_1')
		transition_a_question_2 = petri_utils.add_transition(net_ip_8, 'a?_2')
		transition_b_exclamation = petri_utils.add_transition(net_ip_8, 'b!')
		transition_b_question_1 = petri_utils.add_transition(net_ip_8, 'b?_1')
		transition_b_question_2 = petri_utils.add_transition(net_ip_8, 'b?_2')

		transition_ackA_exclamation = petri_utils.add_transition(net_ip_8, 'ackA!')
		transition_ackA_question = petri_utils.add_transition(net_ip_8, 'ackA?')
		transition_ackB_question = petri_utils.add_transition(net_ip_8, 'ackB?')
		transition_ackB_exclamation = petri_utils.add_transition(net_ip_8, 'ackB!')

		transition_aR_question  = petri_utils.add_transition(net_ip_8, 'aR?')
		transition_aR_exclamation = petri_utils.add_transition(net_ip_8, 'aR!')
		transition_bR_question  = petri_utils.add_transition(net_ip_8, 'bR?')
		transition_bR_exclamation = petri_utils.add_transition(net_ip_8, 'bR!')

		t1 = petri_utils.add_transition(net_ip_8, 't1')
		t2 = petri_utils.add_transition(net_ip_8, 't2')

	# Create arcs
		#left part

		petri_utils.add_arc_from_to(place_1, transition_a_exclamation, net_ip_8)
		petri_utils.add_arc_from_to(transition_a_exclamation, place_2, net_ip_8)
		petri_utils.add_arc_from_to(place_2, transition_bR_question, net_ip_8)
		petri_utils.add_arc_from_to(place_2, transition_ackA_question, net_ip_8)
		petri_utils.add_arc_from_to(transition_bR_question, place_3, net_ip_8)
		petri_utils.add_arc_from_to(place_3, transition_a_question_2, net_ip_8)
		petri_utils.add_arc_from_to(transition_a_question_2, place_A1, net_ip_8)
		petri_utils.add_arc_from_to(transition_ackA_question, place_A1, net_ip_8)



		# right part
		petri_utils.add_arc_from_to(place_13, transition_b_exclamation, net_ip_8)
		petri_utils.add_arc_from_to(transition_b_exclamation, place_14, net_ip_8)
		petri_utils.add_arc_from_to(place_14, transition_aR_question, net_ip_8)
		petri_utils.add_arc_from_to(place_14, transition_ackB_question, net_ip_8)
		petri_utils.add_arc_from_to(transition_aR_question, place_15, net_ip_8)
		petri_utils.add_arc_from_to(place_15, transition_b_question_2, net_ip_8)
		petri_utils.add_arc_from_to(transition_b_question_2, place_A3, net_ip_8)
		petri_utils.add_arc_from_to(transition_ackB_question, place_A3, net_ip_8)

		# center part
		petri_utils.add_arc_from_to(place_4, transition_a_question_1, net_ip_8)
		petri_utils.add_arc_from_to(place_4, transition_b_question_1, net_ip_8)

		petri_utils.add_arc_from_to(transition_a_question_1, place_5, net_ip_8)
		petri_utils.add_arc_from_to(place_5, transition_aR_exclamation, net_ip_8)
		petri_utils.add_arc_from_to(transition_aR_exclamation, place_9, net_ip_8)
		petri_utils.add_arc_from_to(place_9, t1, net_ip_8)

		petri_utils.add_arc_from_to(transition_a_question_1, place_6, net_ip_8)
		petri_utils.add_arc_from_to(place_6, transition_ackA_exclamation, net_ip_8)
		petri_utils.add_arc_from_to(transition_ackA_exclamation, place_10, net_ip_8)
		petri_utils.add_arc_from_to(place_10, t1, net_ip_8)

		petri_utils.add_arc_from_to(transition_b_question_1, place_7, net_ip_8)
		petri_utils.add_arc_from_to(place_7, transition_ackB_exclamation, net_ip_8)
		petri_utils.add_arc_from_to(transition_ackB_exclamation, place_11, net_ip_8)
		petri_utils.add_arc_from_to(place_11, t2, net_ip_8)

		petri_utils.add_arc_from_to(transition_b_question_1, place_8, net_ip_8)
		petri_utils.add_arc_from_to(place_8, transition_bR_exclamation, net_ip_8)
		petri_utils.add_arc_from_to(transition_bR_exclamation, place_12, net_ip_8)
		petri_utils.add_arc_from_to(place_12, t2, net_ip_8)

		petri_utils.add_arc_from_to(t1, place_A2, net_ip_8)
		petri_utils.add_arc_from_to(t2, place_A2, net_ip_8)

		# interaction arcs
		petri_utils.add_arc_from_to(transition_a_exclamation, place_a, net_ip_8)
		petri_utils.add_arc_from_to(transition_b_exclamation, place_b, net_ip_8)

		petri_utils.add_arc_from_to(place_a, transition_a_question_1, net_ip_8)
		petri_utils.add_arc_from_to(place_a, transition_a_question_2, net_ip_8)

		petri_utils.add_arc_from_to(place_b, transition_b_question_1, net_ip_8)
		petri_utils.add_arc_from_to(place_b, transition_b_question_2, net_ip_8)

		petri_utils.add_arc_from_to(transition_bR_exclamation, place_bR, net_ip_8)
		petri_utils.add_arc_from_to(place_bR, transition_bR_question, net_ip_8)

		petri_utils.add_arc_from_to(transition_aR_exclamation, place_aR, net_ip_8)
		petri_utils.add_arc_from_to(place_aR, transition_aR_question, net_ip_8)

		petri_utils.add_arc_from_to(transition_ackA_exclamation, place_ackA, net_ip_8)
		petri_utils.add_arc_from_to(place_ackA, transition_ackA_question, net_ip_8)

		petri_utils.add_arc_from_to(transition_ackB_exclamation, place_ackB, net_ip_8)
		petri_utils.add_arc_from_to(place_ackB, transition_ackB_question, net_ip_8)

	# Define the initial and final marking
		initial_marking = pm4py.objects.petri_net.obj.Marking()
		initial_marking[place_A1] = 1  # Initial token in place A1

		final_marking = pm4py.objects.petri_net.obj.Marking()
		final_marking[place_A3] = 1  # Final token in place A3

		return net_ip_8, initial_marking, final_marking

	@staticmethod
	def create_ip_9_petri_net(): # dont really get what the meant todo
		# Create a Petri net
		net_ip_9 = PetriNet("IP-9")

		# Add places to the Petri net
		place_1 = petri_utils.add_place(net_ip_9, 'P1')
		place_2 = petri_utils.add_place(net_ip_9, 'P2')
		place_3 = petri_utils.add_place(net_ip_9, 'P3')
		place_4 = petri_utils.add_place(net_ip_9, 'P4')
		place_5 = petri_utils.add_place(net_ip_9, 'P5')
		place_6 = petri_utils.add_place(net_ip_9, 'P6')

		place_A1 = petri_utils.add_place(net_ip_9, 'A1')
		place_A2 = petri_utils.add_place(net_ip_9, 'A2')

		place_a = petri_utils.add_place(net_ip_9, 'Pa')
		place_b = petri_utils.add_place(net_ip_9, 'Pb')

		# Add transitions to the Petri net
		transition_a_exclamation = petri_utils.add_transition(net_ip_9, 'a!')
		transition_a_question = petri_utils.add_transition(net_ip_9, 'a?')
		transition_b_exclamation = petri_utils.add_transition(net_ip_9, 'b!')
		transition_b_question = petri_utils.add_transition(net_ip_9, 'b?')
		transition_s = petri_utils.add_transition(net_ip_9, 's')

		# Create arcs

		petri_utils.add_arc_from_to(place_1, transition_s, net_ip_9)
		petri_utils.add_arc_from_to(place_2, transition_s, net_ip_9)
		petri_utils.add_arc_from_to(transition_s, place_3, net_ip_9)
		petri_utils.add_arc_from_to(transition_s, place_4, net_ip_9)

		petri_utils.add_arc_from_to(place_3, transition_a_exclamation, net_ip_9)
		petri_utils.add_arc_from_to(place_4, transition_a_question, net_ip_9)

		petri_utils.add_arc_from_to(transition_a_exclamation, place_5, net_ip_9)
		petri_utils.add_arc_from_to(transition_a_question, place_6, net_ip_9)
		petri_utils.add_arc_from_to(place_5, transition_b_question, net_ip_9)
		petri_utils.add_arc_from_to(place_6, transition_b_exclamation, net_ip_9)
		petri_utils.add_arc_from_to(transition_b_question, place_A1, net_ip_9)
		petri_utils.add_arc_from_to(transition_b_exclamation, place_A2, net_ip_9)

		# interaction arcs

		petri_utils.add_arc_from_to(transition_a_exclamation, place_a, net_ip_9)
		petri_utils.add_arc_from_to(place_a, transition_a_question, net_ip_9)

		petri_utils.add_arc_from_to(transition_b_exclamation, place_b, net_ip_9)
		petri_utils.add_arc_from_to(place_b, transition_b_question, net_ip_9)

	# Define the initial and final marking
		initial_marking = pm4py.objects.petri_net.obj.Marking()
		initial_marking[place_A1] = 1  # Initial token in place A1

		final_marking = pm4py.objects.petri_net.obj.Marking()
		final_marking[place_A2] = 1  # Final token in place A2

		return net_ip_9, initial_marking, final_marking

	@staticmethod
	def create_ip_10_petri_net():
		# Create a Petri net
		net_ip_10 = PetriNet("IP-10")


		# Add places to the Petri net
		place_A1 = petri_utils.add_place(net_ip_10, 'A1')
		place_A2 = petri_utils.add_place(net_ip_10, 'A2')
		place_a = petri_utils.add_place(net_ip_10, 'a')
		place_b = petri_utils.add_place(net_ip_10, 'b')
		place_1 = petri_utils.add_place(net_ip_10, 'P1')
		place_2 = petri_utils.add_place(net_ip_10, 'P2')
		place_3 = petri_utils.add_place(net_ip_10, 'P3')
		place_4 = petri_utils.add_place(net_ip_10, 'P4')
		place_5 = petri_utils.add_place(net_ip_10, 'P5')
		place_6 = petri_utils.add_place(net_ip_10, 'P6')

		# Add transitions to the Petri net
		transition_a_exclamation = petri_utils.add_transition(net_ip_10, 'a!')
		transition_a_question = petri_utils.add_transition(net_ip_10, 'a?')
		transition_b_exclamation = petri_utils.add_transition(net_ip_10, 'b!')
		transition_b_question = petri_utils.add_transition(net_ip_10, 'b?')

		transition_s_question = petri_utils.add_transition(net_ip_10, 's')


		# Create arcs
		petri_utils.add_arc_from_to(place_1, transition_a_exclamation, net_ip_10)
		petri_utils.add_arc_from_to(transition_a_exclamation, place_2, net_ip_10)
		petri_utils.add_arc_from_to(place_2, transition_b_question, net_ip_10)
		petri_utils.add_arc_from_to(transition_b_question, place_5, net_ip_10)

		petri_utils.add_arc_from_to(place_3, transition_a_question, net_ip_10)
		petri_utils.add_arc_from_to(transition_a_question, place_4, net_ip_10)
		petri_utils.add_arc_from_to(place_4, transition_b_exclamation, net_ip_10)
		petri_utils.add_arc_from_to(transition_b_exclamation, place_6, net_ip_10)

		petri_utils.add_arc_from_to(transition_a_exclamation, place_a, net_ip_10)
		petri_utils.add_arc_from_to(place_a, transition_a_question, net_ip_10)

		petri_utils.add_arc_from_to(transition_b_exclamation, place_b, net_ip_10)
		petri_utils.add_arc_from_to(place_b, transition_b_question, net_ip_10)

		petri_utils.add_arc_from_to(place_5, transition_s_question, net_ip_10)
		petri_utils.add_arc_from_to(place_6, transition_s_question, net_ip_10)
		petri_utils.add_arc_from_to(transition_s_question, place_A1, net_ip_10)
		petri_utils.add_arc_from_to(transition_s_question, place_A2, net_ip_10) # todo this arc and the place A2 is optional


		# Define the initial and final marking
		initial_marking = pm4py.objects.petri_net.obj.Marking()
		initial_marking[place_A1] = 1  # Initial token in place A1

		final_marking = pm4py.objects.petri_net.obj.Marking()
		final_marking[place_A2] = 1  # Final token in place A2

		return net_ip_10, initial_marking, final_marking

	@staticmethod
	def create_ip_11_petri_net():
		# Create a Petri net
		net_ip_11 = PetriNet("IP-11")

		# Add places to the Petri net
		place_1 = petri_utils.add_place(net_ip_11, 'P1')
		place_2 = petri_utils.add_place(net_ip_11, 'P2')
		place_3 = petri_utils.add_place(net_ip_11, 'P3')
		place_4 = petri_utils.add_place(net_ip_11, 'P4')
		place_5 = petri_utils.add_place(net_ip_11, 'P5')
		place_6 = petri_utils.add_place(net_ip_11, 'P6')
		place_7 = petri_utils.add_place(net_ip_11, 'P7')
		place_8 = petri_utils.add_place(net_ip_11, 'P8')
		place_9 = petri_utils.add_place(net_ip_11, 'P9')
		place_10 = petri_utils.add_place(net_ip_11, 'P10')

		place_a = petri_utils.add_place(net_ip_11, 'a')
		place_b = petri_utils.add_place(net_ip_11, 'b')

		place_A1 = petri_utils.add_place(net_ip_11, 'A1')
		place_A2 = petri_utils.add_place(net_ip_11, 'A2')


		# Add transitions to the Petri net
		transition_a_exclamation = petri_utils.add_transition(net_ip_11, 'a!')
		transition_a_question = petri_utils.add_transition(net_ip_11, 'a?')
		transition_b_exclamation = petri_utils.add_transition(net_ip_11, 'b!')
		transition_b_question = petri_utils.add_transition(net_ip_11, 'b?')
		transition_s = petri_utils.add_transition(net_ip_11, 's')

		t1 = petri_utils.add_transition(net_ip_11, 't1')
		t2 = petri_utils.add_transition(net_ip_11, 't2')

		# Create arcs
		# left side
		petri_utils.add_arc_from_to(place_1, t1, net_ip_11)
		petri_utils.add_arc_from_to(t1, place_2, net_ip_11)
		petri_utils.add_arc_from_to(place_2, transition_a_exclamation, net_ip_11)
		petri_utils.add_arc_from_to(t1, place_3, net_ip_11)
		petri_utils.add_arc_from_to(place_3, transition_s, net_ip_11)

		petri_utils.add_arc_from_to(transition_a_exclamation, place_4, net_ip_11)
		petri_utils.add_arc_from_to(place_4, transition_b_question, net_ip_11)
		petri_utils.add_arc_from_to(transition_b_question, place_A1, net_ip_11)

		#right side
		petri_utils.add_arc_from_to(place_5, t2, net_ip_11)
		petri_utils.add_arc_from_to(t2, place_6, net_ip_11)
		petri_utils.add_arc_from_to(place_6, transition_a_question, net_ip_11)
		petri_utils.add_arc_from_to(t2, place_7, net_ip_11)
		petri_utils.add_arc_from_to(place_7, transition_s, net_ip_11)

		petri_utils.add_arc_from_to(transition_a_question, place_8, net_ip_11)
		petri_utils.add_arc_from_to(place_8, transition_b_exclamation, net_ip_11)
		petri_utils.add_arc_from_to(transition_b_exclamation, place_A2, net_ip_11)


		# interaction arcs

		petri_utils.add_arc_from_to(transition_a_exclamation, place_a, net_ip_11)
		petri_utils.add_arc_from_to(place_a, transition_a_question, net_ip_11)

		petri_utils.add_arc_from_to(transition_b_exclamation, place_b, net_ip_11)
		petri_utils.add_arc_from_to(place_b, transition_b_question, net_ip_11)

		petri_utils.add_arc_from_to(transition_s, place_9, net_ip_11)
		petri_utils.add_arc_from_to(transition_s, place_10, net_ip_11) # todo optional

		# Define the initial and final marking
		initial_marking = pm4py.objects.petri_net.obj.Marking()
		initial_marking[place_A1] = 1  # Initial token in place A1

		final_marking = pm4py.objects.petri_net.obj.Marking()
		final_marking[place_A2] = 1  # Final token in place A2

		return net_ip_11, initial_marking, final_marking


	@staticmethod
	def create_ip_12_petri_net():
		# Create a Petri net
		net_ip_12 = PetriNet("IP-12")

		# Add places to the Petri net
		place_A1 = petri_utils.add_place(net_ip_12, 'A1')
		place_A2 = petri_utils.add_place(net_ip_12, 'A2')

		place_1 = petri_utils.add_place(net_ip_12, 'P1')
		place_2 = petri_utils.add_place(net_ip_12, 'P2')
		place_3 = petri_utils.add_place(net_ip_12, 'P3')
		place_4 = petri_utils.add_place(net_ip_12, 'P4')
		place_5 = petri_utils.add_place(net_ip_12, 'P5')
		place_6 = petri_utils.add_place(net_ip_12, 'P6')

		place_a = petri_utils.add_place(net_ip_12, 'a')
		place_b = petri_utils.add_place(net_ip_12, 'b')

		# Add transitions to the Petri net
		transition_a_exclamation = petri_utils.add_transition(net_ip_12, 'a!')
		transition_a_question = petri_utils.add_transition(net_ip_12, 'a?')
		transition_b_exclamation = petri_utils.add_transition(net_ip_12, 'b!')
		transition_b_question = petri_utils.add_transition(net_ip_12, 'b?')

		transition_s = petri_utils.add_transition(net_ip_12, 's')

		t1 = petri_utils.add_transition(net_ip_12, 't1')
		t2 = petri_utils.add_transition(net_ip_12, 't2')

		# Create arcs
		petri_utils.add_arc_from_to(place_1, transition_a_exclamation, net_ip_12)
		petri_utils.add_arc_from_to(transition_a_exclamation, place_2, net_ip_12)
		petri_utils.add_arc_from_to(place_2, transition_b_question, net_ip_12)
		petri_utils.add_arc_from_to(transition_b_question, place_A1, net_ip_12)

		petri_utils.add_arc_from_to(place_3, transition_a_question, net_ip_12)
		petri_utils.add_arc_from_to(transition_a_question, place_4, net_ip_12)
		petri_utils.add_arc_from_to(place_4, transition_b_exclamation, net_ip_12)
		petri_utils.add_arc_from_to(transition_b_exclamation, place_A2, net_ip_12)

		# center
		petri_utils.add_arc_from_to(place_5, t1, net_ip_12)
		petri_utils.add_arc_from_to(place_6, t2, net_ip_12)
		petri_utils.add_arc_from_to(t1, place_A1, net_ip_12)
		petri_utils.add_arc_from_to(t2, place_A2, net_ip_12)


	# interaction
		petri_utils.add_arc_from_to(transition_a_exclamation, place_a, net_ip_12)
		petri_utils.add_arc_from_to(place_a, transition_a_question, net_ip_12)

		petri_utils.add_arc_from_to(transition_b_exclamation, place_b, net_ip_12)
		petri_utils.add_arc_from_to(place_b, transition_b_question, net_ip_12)

		petri_utils.add_arc_from_to(place_3, transition_s, net_ip_12)
		petri_utils.add_arc_from_to(place_1, transition_s, net_ip_12)
		petri_utils.add_arc_from_to(transition_s, place_5, net_ip_12)
		petri_utils.add_arc_from_to(transition_s, place_6, net_ip_12)

	# Define the initial and final marking
		initial_marking = pm4py.objects.petri_net.obj.Marking()
		initial_marking[place_A1] = 1  # Initial token in place A1

		final_marking = pm4py.objects.petri_net.obj.Marking()
		final_marking[place_A2] = 1  # Final token in place A2

		return net_ip_12, initial_marking, final_marking


	@staticmethod
	def get_patterns() -> list:
		patterns = []
		patterns.append(interface_patterns.create_ip_1_petri_net())
		patterns.append(interface_patterns.create_ip_2_petri_net())
		patterns.append(interface_patterns.create_ip_2b_petri_net())
		patterns.append(interface_patterns.create_ip_3_petri_net())
		patterns.append(interface_patterns.create_ip_4_petri_net())
		patterns.append(interface_patterns.create_ip_5_petri_net())
		patterns.append(interface_patterns.create_ip_6_petri_net())
		patterns.append(interface_patterns.create_ip_7_petri_net())
		patterns.append(interface_patterns.create_ip_8_petri_net())
		patterns.append(interface_patterns.create_ip_9_petri_net())
		patterns.append(interface_patterns.create_ip_10_petri_net())
		patterns.append(interface_patterns.create_ip_11_petri_net())
		patterns.append(interface_patterns.create_ip_12_petri_net())
		return patterns

# net,_,_ = interface_patterns.create_ip_2b_petri_net()
# pm4py.view_petri_net(net, format="png",  debug=True)
# net,_,_ = interface_patterns.create_ip_2_petri_net()
# pm4py.view_petri_net(net, format="png",  debug=True)