(define (domain gripper)

  (:requirements
    :typing
  )

  (:types location
        gripper
        object)

  (:constants
    r1 r2 - location
    g  - gripper
    b1 b2   - object

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
  )

(:action move
:parameters (?from - location ?to - location)
:precondition (and(atrob ?from)(adj ?from ?to)(room ?from))
:effect (oneof
  (d2(and (not (atrob ?from))(atrob ?to)))

  (d1(and (not (atrob ?from))(atrob ?to) (scratch)))
)
)


(:action pick
:parameters (?b - object ?r - location ?g - gripper)
:precondition (and (atrob ?r) (ball ?b) ( gripper ?g) (at ?b ?r) (free ?g))
:effect (oneof

    (d2(and (carry ?b ?g) (not(at ?b ?r)) (not(free ?g))))

    (d1(and (at ?b ?r) (free ?g) (not(carry ?b ?g))))
)
)







(:action drop
:parameters (?b - object ?r - room ?g - gripper)
:precondition (and(ball ?b)(room ?r) (gripper ?g)(atrob ?r) (carry ?b ?g))
:effect (oneof

  (d2(and (at ?b ?r) (free ?g) (not(carry ?b ?g))))

  (d1(and (at ?b ?r) (not (free ?g))   (carry ?b ?g)))
)
)









)




