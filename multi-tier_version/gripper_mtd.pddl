(define (domain gripper)
	(:requirements :typing)
	(:types 
		 location gripper object
	)
	(:constants 
		b1 b2 - object
 		g - gripper
 		r1 r2 - location
	)
	(:predicates
		(atrob ?loc - location)
		(spare-in ?loc - location)
		(adj ?from - location ?to - location)
		(room ?r - location)
		(ball ?o - object)
		(gripper ?gr - gripper)
		(at ?o - object ?r - location)
		(free ?gr - gripper)
		(carry ?o - object ?gr - gripper)
		(scratch)
		(end)
		(act)
		(l_d2)
		(e_d2)
		(eff_d2_move)
		(eff_d2_pick)
		(eff_d2_drop)
		(l_d1)
		(e_d1)
		(eff_d1_move)
		(eff_d1_pick)
		(eff_d1_drop)
		(u_move)
		(u_pick)
		(u_drop)
	)
	(:action continue_d2 
		:parameters ()
		:precondition (and  (not (act)) (l_d2) (not (eff_d2_move)) (not (eff_d2_pick)) (not (eff_d2_drop)) (not (eff_d1_move)) (not (eff_d1_pick)) (not (eff_d1_drop)) (or (e_d2)))
		:effect (and (act) (not (e_d2)) (not (e_d1)))
	)
	(:action continue_d1 
		:parameters ()
		:precondition (and  (not (act)) (l_d1) (not (eff_d2_move)) (not (eff_d2_pick)) (not (eff_d2_drop)) (not (eff_d1_move)) (not (eff_d1_pick)) (not (eff_d1_drop)) (or (e_d2) (e_d1)))
		:effect (and (act) (not (e_d2)) (not (e_d1)))
	)
	(:action degrade_d2_d1 
		:parameters ()
		:precondition (and  (not (act)) (l_d2) (e_d1) (not (eff_d2_move)) (not (eff_d2_pick)) (not (eff_d2_drop)) (not (eff_d1_move)) (not (eff_d1_pick)) (not (eff_d1_drop)))
		:effect (and (act) (l_d1) (not (l_d2)) (not (e_d2)) (not (e_d1)))
	)
	(:action move_unfair_ 
		:parameters ()
		:precondition (and  (act) (u_move))
		:effect (oneof (and (eff_d2_move) (not (act))) (and (eff_d1_move) (not (act))))
	)
	(:action move_d2 
		:parameters (?from - location ?to - location)
		:precondition (and  (atrob ?from) (adj ?from ?to) (room ?from) (l_d2) (act) (not (u_move)) (not (u_pick)) (not (u_drop)))
		:effect (oneof (and (not (atrob ?from)) (atrob ?to)) (u_move))
	)
	(:action move_d1 
		:parameters (?from - location ?to - location)
		:precondition (and  (atrob ?from) (adj ?from ?to) (room ?from) (l_d1) (act) (not (u_move)) (not (u_pick)) (not (u_drop)))
		:effect (oneof (and (not (atrob ?from)) (atrob ?to)) (and (not (atrob ?from)) (atrob ?to) (scratch)))
	)
	(:action move_eff_d2_explained_by_d2 
		:parameters (?from - location ?to - location)
		:precondition (and  (atrob ?from) (adj ?from ?to) (room ?from) (eff_d2_move))
		:effect (and (not (atrob ?from)) (atrob ?to) (e_d2) (not (eff_d2_move)) (not (act)) (not (u_move)))
	)
	(:action move_eff_d1_explained_by_d2 
		:parameters (?from - location ?to - location)
		:precondition (and  (atrob ?from) (adj ?from ?to) (room ?from) (eff_d1_move) (scratch))
		:effect (and (not (atrob ?from)) (atrob ?to) (scratch) (e_d2) (not (eff_d1_move)) (not (act)) (not (u_move)))
	)
	(:action move_eff_d1_explained_by_d1 
		:parameters (?from - location ?to - location)
		:precondition (and  (atrob ?from) (adj ?from ?to) (room ?from) (eff_d1_move) (or (not (scratch))))
		:effect (and (not (atrob ?from)) (atrob ?to) (scratch) (e_d1) (not (eff_d1_move)) (not (act)) (not (u_move)))
	)
	(:action pick_unfair_ 
		:parameters ()
		:precondition (and  (act) (u_pick))
		:effect (oneof (and (eff_d2_pick) (not (act))) (and (eff_d1_pick) (not (act))))
	)
	(:action pick_d2 
		:parameters (?b - object ?r - location ?g - gripper)
		:precondition (and  (atrob ?r) (ball ?b) (gripper ?g) (at ?b ?r) (free ?g) (l_d2) (act) (not (u_move)) (not (u_pick)) (not (u_drop)))
		:effect (oneof (and (carry ?b ?g) (not (at ?b ?r)) (not (free ?g))) (u_pick))
	)
	(:action pick_d1 
		:parameters (?b - object ?r - location ?g - gripper)
		:precondition (and  (atrob ?r) (ball ?b) (gripper ?g) (at ?b ?r) (free ?g) (l_d1) (act) (not (u_move)) (not (u_pick)) (not (u_drop)))
		:effect (oneof (and (carry ?b ?g) (not (at ?b ?r)) (not (free ?g))) (and (at ?b ?r) (free ?g) (not (carry ?b ?g))))
	)
	(:action pick_eff_d2_explained_by_d2 
		:parameters (?b - object ?r - location ?g - gripper)
		:precondition (and  (atrob ?r) (ball ?b) (gripper ?g) (at ?b ?r) (free ?g) (eff_d2_pick))
		:effect (and (carry ?b ?g) (not (at ?b ?r)) (not (free ?g)) (e_d2) (not (eff_d2_pick)) (not (act)) (not (u_pick)))
	)
	(:action pick_eff_d1_explained_by_d2 
		:parameters (?b - object ?r - location ?g - gripper)
		:precondition (and  (atrob ?r) (ball ?b) (gripper ?g) (at ?b ?r) (free ?g) (eff_d1_pick) (at ?b ?r) (free ?g) (not (carry ?b ?g)) (carry ?b ?g) (not (at ?b ?r)) (not (free ?g)))
		:effect (and (at ?b ?r) (free ?g) (not (carry ?b ?g)) (e_d2) (not (eff_d1_pick)) (not (act)) (not (u_pick)))
	)
	(:action pick_eff_d1_explained_by_d1 
		:parameters (?b - object ?r - location ?g - gripper)
		:precondition (and  (atrob ?r) (ball ?b) (gripper ?g) (at ?b ?r) (free ?g) (eff_d1_pick) (or (not (at ?b ?r)) (not (free ?g)) (carry ?b ?g) (not (carry ?b ?g)) (at ?b ?r) (free ?g)))
		:effect (and (at ?b ?r) (free ?g) (not (carry ?b ?g)) (e_d1) (not (eff_d1_pick)) (not (act)) (not (u_pick)))
	)
	(:action drop_unfair_ 
		:parameters ()
		:precondition (and  (act) (u_drop))
		:effect (oneof (and (eff_d2_drop) (not (act))) (and (eff_d1_drop) (not (act))))
	)
	(:action drop_d2 
		:parameters (?b - object ?r - room ?g - gripper)
		:precondition (and  (ball ?b) (room ?r) (gripper ?g) (atrob ?r) (carry ?b ?g) (l_d2) (act) (not (u_move)) (not (u_pick)) (not (u_drop)))
		:effect (oneof (and (at ?b ?r) (free ?g) (not (carry ?b ?g))) (u_drop))
	)
	(:action drop_d1 
		:parameters (?b - object ?r - room ?g - gripper)
		:precondition (and  (ball ?b) (room ?r) (gripper ?g) (atrob ?r) (carry ?b ?g) (l_d1) (act) (not (u_move)) (not (u_pick)) (not (u_drop)))
		:effect (oneof (and (at ?b ?r) (free ?g) (not (carry ?b ?g))) (and (at ?b ?r) (not (free ?g)) (carry ?b ?g)))
	)
	(:action drop_eff_d2_explained_by_d2 
		:parameters (?b - object ?r - room ?g - gripper)
		:precondition (and  (ball ?b) (room ?r) (gripper ?g) (atrob ?r) (carry ?b ?g) (eff_d2_drop))
		:effect (and (at ?b ?r) (free ?g) (not (carry ?b ?g)) (e_d2) (not (eff_d2_drop)) (not (act)) (not (u_drop)))
	)
	(:action drop_eff_d1_explained_by_d2 
		:parameters (?b - object ?r - room ?g - gripper)
		:precondition (and  (ball ?b) (room ?r) (gripper ?g) (atrob ?r) (carry ?b ?g) (eff_d1_drop) (not (free ?g)) (carry ?b ?g) (free ?g) (not (carry ?b ?g)))
		:effect (and (at ?b ?r) (not (free ?g)) (carry ?b ?g) (e_d2) (not (eff_d1_drop)) (not (act)) (not (u_drop)))
	)
	(:action drop_eff_d1_explained_by_d1 
		:parameters (?b - object ?r - room ?g - gripper)
		:precondition (and  (ball ?b) (room ?r) (gripper ?g) (atrob ?r) (carry ?b ?g) (eff_d1_drop) (or (free ?g) (not (carry ?b ?g)) (not (free ?g)) (carry ?b ?g)))
		:effect (and (at ?b ?r) (not (free ?g)) (carry ?b ?g) (e_d1) (not (eff_d1_drop)) (not (act)) (not (u_drop)))
	)
	(:action check_goal_d2 
		:parameters ()
		:precondition (and  (atrob r2) (at b1 r2) (l_d2) (act))
		:effect (end)
	)
	(:action check_goal_d1 
		:parameters ()
		:precondition (and  (atrob r2) (l_d1) (act))
		:effect (end)
	)
)
