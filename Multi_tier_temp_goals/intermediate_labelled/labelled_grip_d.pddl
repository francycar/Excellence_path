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
		(q2 ?loc96 - location ?gr92 - gripper ?loc14 - location)
		(q1 ?loc96 - location ?gr92 - gripper ?loc14 - location)
		(q3 ?loc96 - location ?gr92 - gripper ?loc14 - location)
		(q4 ?loc96 - location ?gr92 - gripper ?loc14 - location)
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
		:parameters (?o27 - object ?r42 - location ?loc27 - location ?gr50 - gripper)
		:precondition (and  (or (and (q1 ?o27 ?r42 ?loc27 ?gr50) (not (at ?o27 ?r42)) (not (atrob ?loc27))) (and (q1 ?o27 ?r42 ?loc27 ?gr50) (not (at ?o27 ?r42)) (atrob ?loc27) (atrob ?r42) (carry ?o27 ?gr50)) (and (q2 ?o27 ?r42 ?loc27 ?gr50) (not (at ?o27 ?r42)) (atrob ?r42) (carry ?o27 ?gr50)) ) (not (turndomain)))
		:effect (and (q1 ?o27 ?r42 ?loc27 ?gr50) (not (q4 ?o27 ?r42 ?loc27 ?gr50)) (not (q2 ?o27 ?r42 ?loc27 ?gr50)) (not (q3 ?o27 ?r42 ?loc27 ?gr50)) (turndomain))
	)
	(:action trans-12 
		:parameters (?o27 - object ?r42 - location ?loc27 - location ?gr50 - gripper)
		:precondition (and  (or (and (q1 ?o27 ?r42 ?loc27 ?gr50) (at ?o27 ?r42) (atrob ?loc27) (not (atrob ?r42))) (and (q1 ?o27 ?r42 ?loc27 ?gr50) (at ?o27 ?r42) (atrob ?loc27) (atrob ?r42) (not (carry ?o27 ?gr50))) (and (q2 ?o27 ?r42 ?loc27 ?gr50) (at ?o27 ?r42) (not (atrob ?r42))) (and (q2 ?o27 ?r42 ?loc27 ?gr50) (at ?o27 ?r42) (atrob ?r42) (not (carry ?o27 ?gr50))) (and (q3 ?o27 ?r42 ?loc27 ?gr50) (atrob ?loc27) (not (atrob ?r42))) (and (q3 ?o27 ?r42 ?loc27 ?gr50) (atrob ?loc27) (atrob ?r42) (not (carry ?o27 ?gr50))) (and (q4 ?o27 ?r42 ?loc27 ?gr50) (not (atrob ?r42))) (and (q4 ?o27 ?r42 ?loc27 ?gr50) (atrob ?r42) (not (carry ?o27 ?gr50))) ) (not (turndomain)))
		:effect (and (q4 ?o27 ?r42 ?loc27 ?gr50) (not (q1 ?o27 ?r42 ?loc27 ?gr50)) (not (q2 ?o27 ?r42 ?loc27 ?gr50)) (not (q3 ?o27 ?r42 ?loc27 ?gr50)) (turndomain))
	)
	(:action trans-22 
		:parameters (?o27 - object ?r42 - location ?loc27 - location ?gr50 - gripper)
		:precondition (and  (or (and (q1 ?o27 ?r42 ?loc27 ?gr50) (not (at ?o27 ?r42)) (atrob ?loc27) (not (atrob ?r42))) (and (q1 ?o27 ?r42 ?loc27 ?gr50) (not (at ?o27 ?r42)) (atrob ?loc27) (atrob ?r42) (not (carry ?o27 ?gr50))) (and (q2 ?o27 ?r42 ?loc27 ?gr50) (not (at ?o27 ?r42)) (not (atrob ?r42))) (and (q2 ?o27 ?r42 ?loc27 ?gr50) (not (at ?o27 ?r42)) (atrob ?r42) (not (carry ?o27 ?gr50))) ) (not (turndomain)))
		:effect (and (q2 ?o27 ?r42 ?loc27 ?gr50) (not (q1 ?o27 ?r42 ?loc27 ?gr50)) (not (q4 ?o27 ?r42 ?loc27 ?gr50)) (not (q3 ?o27 ?r42 ?loc27 ?gr50)) (turndomain))
	)
	(:action trans-32 
		:parameters (?o27 - object ?r42 - location ?loc27 - location ?gr50 - gripper)
		:precondition (and  (or (and (q1 ?o27 ?r42 ?loc27 ?gr50) (at ?o27 ?r42) (not (atrob ?loc27))) (and (q1 ?o27 ?r42 ?loc27 ?gr50) (at ?o27 ?r42) (atrob ?loc27) (atrob ?r42) (carry ?o27 ?gr50)) (and (q2 ?o27 ?r42 ?loc27 ?gr50) (at ?o27 ?r42) (atrob ?r42) (carry ?o27 ?gr50)) (and (q3 ?o27 ?r42 ?loc27 ?gr50) (not (atrob ?loc27))) (and (q3 ?o27 ?r42 ?loc27 ?gr50) (atrob ?loc27) (atrob ?r42) (carry ?o27 ?gr50)) (and (q4 ?o27 ?r42 ?loc27 ?gr50) (atrob ?r42) (carry ?o27 ?gr50)) ) (not (turndomain)))
		:effect (and (q3 ?o27 ?r42 ?loc27 ?gr50) (not (q1 ?o27 ?r42 ?loc27 ?gr50)) (not (q4 ?o27 ?r42 ?loc27 ?gr50)) (not (q2 ?o27 ?r42 ?loc27 ?gr50)) (turndomain))
	)
	(:action trans-01 
		:parameters (?loc96 - location ?gr92 - gripper ?loc14 - location)
		:precondition (and  (or (and (q1 ?loc96 ?gr92 ?loc14) (not (atrob ?loc96)) (free ?gr92) (not (atrob ?loc14))) (and (q1 ?loc96 ?gr92 ?loc14) (not (atrob ?loc96)) (free ?gr92) (atrob ?loc14) (not (scratch))) (and (q2 ?loc96 ?gr92 ?loc14) (not (atrob ?loc96)) (not (atrob ?loc14))) (and (q2 ?loc96 ?gr92 ?loc14) (not (atrob ?loc96)) (atrob ?loc14) (not (scratch))) ) (not (turndomain)))
		:effect (and (q2 ?loc96 ?gr92 ?loc14) (not (q1 ?loc96 ?gr92 ?loc14)) (not (q3 ?loc96 ?gr92 ?loc14)) (not (q4 ?loc96 ?gr92 ?loc14)) (turndomain))
	)
	(:action trans-11 
		:parameters (?loc96 - location ?gr92 - gripper ?loc14 - location)
		:precondition (and  (or (and (q1 ?loc96 ?gr92 ?loc14) (not (atrob ?loc96)) (not (free ?gr92))) (and (q1 ?loc96 ?gr92 ?loc14) (not (atrob ?loc96)) (free ?gr92) (atrob ?loc14) (scratch)) (and (q2 ?loc96 ?gr92 ?loc14) (not (atrob ?loc96)) (atrob ?loc14) (scratch)) ) (not (turndomain)))
		:effect (and (q1 ?loc96 ?gr92 ?loc14) (not (q2 ?loc96 ?gr92 ?loc14)) (not (q3 ?loc96 ?gr92 ?loc14)) (not (q4 ?loc96 ?gr92 ?loc14)) (turndomain))
	)
	(:action trans-21 
		:parameters (?loc96 - location ?gr92 - gripper ?loc14 - location)
		:precondition (and  (or (and (q1 ?loc96 ?gr92 ?loc14) (atrob ?loc96) (not (free ?gr92))) (and (q1 ?loc96 ?gr92 ?loc14) (atrob ?loc96) (free ?gr92) (atrob ?loc14) (scratch)) (and (q2 ?loc96 ?gr92 ?loc14) (atrob ?loc96) (atrob ?loc14) (scratch)) (and (q3 ?loc96 ?gr92 ?loc14) (not (free ?gr92))) (and (q3 ?loc96 ?gr92 ?loc14) (free ?gr92) (atrob ?loc14) (scratch)) (and (q4 ?loc96 ?gr92 ?loc14) (atrob ?loc14) (scratch)) ) (not (turndomain)))
		:effect (and (q3 ?loc96 ?gr92 ?loc14) (not (q2 ?loc96 ?gr92 ?loc14)) (not (q1 ?loc96 ?gr92 ?loc14)) (not (q4 ?loc96 ?gr92 ?loc14)) (turndomain))
	)
	(:action trans-31 
		:parameters (?loc96 - location ?gr92 - gripper ?loc14 - location)
		:precondition (and  (or (and (q1 ?loc96 ?gr92 ?loc14) (atrob ?loc96) (free ?gr92) (not (atrob ?loc14))) (and (q1 ?loc96 ?gr92 ?loc14) (atrob ?loc96) (free ?gr92) (atrob ?loc14) (not (scratch))) (and (q2 ?loc96 ?gr92 ?loc14) (atrob ?loc96) (not (atrob ?loc14))) (and (q2 ?loc96 ?gr92 ?loc14) (atrob ?loc96) (atrob ?loc14) (not (scratch))) (and (q3 ?loc96 ?gr92 ?loc14) (free ?gr92) (not (atrob ?loc14))) (and (q3 ?loc96 ?gr92 ?loc14) (free ?gr92) (atrob ?loc14) (not (scratch))) (and (q4 ?loc96 ?gr92 ?loc14) (not (atrob ?loc14))) (and (q4 ?loc96 ?gr92 ?loc14) (atrob ?loc14) (not (scratch))) ) (not (turndomain)))
		:effect (and (q4 ?loc96 ?gr92 ?loc14) (not (q2 ?loc96 ?gr92 ?loc14)) (not (q1 ?loc96 ?gr92 ?loc14)) (not (q3 ?loc96 ?gr92 ?loc14)) (turndomain))
	)
)
