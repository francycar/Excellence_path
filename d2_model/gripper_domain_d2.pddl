(define (domain gripper)
  (:requirements :typing :strips :non-deterministic)
  (:types location
          gripper
          object)
  
  
  
  (:predicates (atrob ?loc - location)
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
    :effect (and (not (atrob ?from))(atrob ?to))
  )



  (:action pick
    :parameters (?b - object ?r - location ?g - gripper)
    :precondition (and (atrob ?r) (ball ?b) ( gripper ?g) (at ?b ?r) (free ?g))
    :effect (and (carry ?b ?g) (not(at ?b ?r)) (not(free ?g)))

  )


  (:action drop
    :parameters (?b - object ?r - location ?g - gripper)
    :precondition (and (ball ?b)(room ?r) ( gripper ?g)(atrob ?r) (carry ?b ?g))
    :effect (and (at ?b ?r) (free ?g) (not(carry ?b ?g)))

  )
  
)













