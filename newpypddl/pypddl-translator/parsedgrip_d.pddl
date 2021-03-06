(define (domain gripper)
	(:requirements :typing)
	(:types 
		 location gripper object
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
		(turndomain)
		(q1 ?loc62 - location)
		(q2 ?loc62 - location)
	)
	(:action move 
		:parameters (?from - location ?to - location)
		:precondition (and  (atrob ?from) (adj ?from ?to) (room ?from) (turndomain))
		:effect (oneof (d2 (and (not (atrob ?from)) (atrob ?to) (not (turndomain))))
		 (d1 (and (not (atrob ?from)) (atrob ?to) (scratch) (not (turndomain))))
		)
	)
	(:action pick 
		:parameters (?b - object ?r - location ?g - gripper)
		:precondition (and  (atrob ?r) (ball ?b) (gripper ?g) (at ?b ?r) (free ?g) (turndomain))
		:effect (oneof (d2 (and (carry ?b ?g) (not (at ?b ?r)) (not (free ?g)) (not (turndomain))))
		 (d1 (and (at ?b ?r) (free ?g) (not (carry ?b ?g)) (not (turndomain))))
		)
	)
	(:action drop 
		:parameters (?b - object ?r - location ?g - gripper)
		:precondition (and  (ball ?b) (room ?r) (gripper ?g) (atrob ?r) (carry ?b ?g) (turndomain))
		:effect (oneof (d2 (and (at ?b ?r) (free ?g) (not (carry ?b ?g)) (not (turndomain))))
		 (d1 (and (at ?b ?r) (not (free ?g)) (carry ?b ?g) (not (turndomain))))
		)
	)
	(:action trans-02 
		:parameters (?o57 - object ?r84 - location)
		:precondition (and  (or (and (q1 ?o57 ?r84) (at ?o57 ?r84) (atrob ?r84)) (q2 ?o57 ?r84)) (not (turndomain)))
		:effect (and (q2 ?o57 ?r84) (not (q1 ?o57 ?r84)) (turndomain))
	)
	(:action trans-12 
		:parameters (?o57 - object ?r84 - location)
		:precondition (and  (or (and (q1 ?o57 ?r84) (not (at ?o57 ?r84))) (and (q1 ?o57 ?r84) (at ?o57 ?r84) (not (atrob ?r84))) ) (not (turndomain)))
		:effect (and (q1 ?o57 ?r84) (not (q2 ?o57 ?r84)) (turndomain))
	)
	(:action trans-01 
		:parameters (?loc62 - location)
		:precondition (and  (q1 ?loc62) (not (atrob ?loc62)) (not (turndomain)))
		:effect (and (q1 ?loc62) (not (q2 ?loc62)) (turndomain))
	)
	(:action trans-11 
		:parameters (?loc62 - location)
		:precondition (and  (or (and (q1 ?loc62) (atrob ?loc62)) (q2 ?loc62)) (not (turndomain)))
		:effect (and (q2 ?loc62) (not (q1 ?loc62)) (turndomain))
	)
)
