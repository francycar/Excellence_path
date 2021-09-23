# This file is part of pypddl-PDDLParser.

# pypddl-parser is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# pypddl-parser is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with pypddl-parser.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import copy

from pddlparser import PDDLParser
from pddlparser import PDDLParser2

from predicate import Predicate
from term      import Term
from literal   import Literal
from action    import Action
from problem import Problem
from mtp import multi_tier_compilation_problem, multi_tier_compilation_domain1, multi_tier_compilation_domain2, multi_tier_compilation_domain3,multi_tier_compilation_domain4, multi_tier_compilation_domain5



# just for testing
def test_change_domain(domain):
    ############################################
    # Let's now create  TYPES AND PREDICATES
    ############################################
    domain.add_type('boxes')
    domain.add_pred('open', [('?x', 'boxes'), ('?z', 'block')])
    domain.del_pred('handempty', 0)

    # print(repr(domain.operators[3]))


    ############################################
    # Let's now create an OPERATOR
    ############################################
    # print(domain.operators[3].precond)
    params = [Term.variable('?x', type='blocks'), Term.variable('?y', type='blocks')]

    precond=[]
    precond.append(Literal(Predicate('=', [Term.variable('?x'), Term.variable('?y')]), False))
    precond.append(Literal(Predicate('on', [Term.variable('?x'), Term.variable('?y')]), True))
    precond.append(Literal(Predicate('clear', [Term.variable('?x')]), True))
    precond.append(Literal(Predicate('handempty', []), True))

    # print(domain.operators[3].effects)
    effect=[]
    effect.append((1.0, Literal(Predicate('holding', [Term.variable('?x')]), True)))
    effect.append((1.0, Literal(Predicate('clear', [Term.variable('?y')]), True)))
    effect.append((1.0, Literal(Predicate('clear', [Term.variable('?x')]), False)))
    effect.append((1.0, Literal(Predicate('handempty', []), False)))
    effect.append((1.0, Literal(Predicate('on', [Term.variable('?x'), Term.variable('?y')]), False)))
    # print(repr(effect))

    domain.add_action('pick-up-b', params, precond, [effect, effect])


# just for testing
def test_change_problem(problem):
    problem.add_object('z', 'block')    # add a new block object

    problem.add_to_init('open', ['1', '2'])
    # print(problem.init)

    problem.add_to_goal('open', ['3', '4'])
    # print(problem.goal)


if __name__ == '__main__':

    
    usage = 'python3 main.py <domain> [<problem>]'
    description = 'Parse a planning domain and problem. ' \
                  '<domain> can store a planning domain or a planning domain and a problem. ' \
                  '<problem> is optional and should contain a problem (when domain only includes the planning domain).' \
                  'A problem can either be a standard planning problem or labeled planning problem (with labeled effects)'
    parser = argparse.ArgumentParser(usage=usage, description=description)

    parser.add_argument('domain-problem',
                        nargs = '+',
                        help='path to at least one file, possibly two, encoding the domain and problem')
    parser.add_argument('--print-domain',
                        action='store_true',
                        default=False,
                        help='print the translated PDDL domain (default: %(default)s). True if --out-problem used')
    parser.add_argument('--print-problem',
                        action='store_true',
                        default=False,
                        help='print the translated PDDL problem (default: %(default)s). True if --out-domain used')
    parser.add_argument('--out-domain',
                        default='',
                        help='filename to write the output PDDL domain')
    parser.add_argument('--out-problem',
                        default='',
                        help='filename to write the output PDDL problem')
    

    parser.add_argument('--out-domain2',
                        default='',
                        help='filename to write the output PDDL domain')
    parser.add_argument('--out-problem2',
                        default='',
                        help='filename to write the output PDDL problem')
    
    parser.add_argument('--out-unitod',
                        default='',
                        help='filename to write the output PDDL domain')
    parser.add_argument('--out-unitop',
                        default='',
                        help='filename to write the output PDDL problem')



    parser.add_argument('--test-changes',
                        action='store_true',
                        default=False,
                        help='do some testing changes to domain and problem (default: %(default)s)')
    parser.add_argument('--multi-tier-compilation',
                        action='store_true',
                        default=False,
                        help='translate labeled PDDL to MTD and MTP (default: %(default)s)')
    
    parser.add_argument('--basic',
                        action='store_true',
                        default=False,
                        help='choose to use basic version')
    

    parser.add_argument('--downgrade',
                        action='store_true',
                        default=False,
                        help='choose to use basic version')
    
    parser.add_argument('--upgrade',
                        action='store_true',
                        default=False,
                        help='choose to use upgrade version')


    parser.add_argument('--refine01',
                        action='store_true',
                        default=False,
                        help='choose to use refine01')
    
    parser.add_argument('--refine02',
                        action='store_true',
                        default=False,
                        help='choose to use refine02')
    
    parser.add_argument('--refine03',
                        action='store_true',
                        default=False,
                        help='choose to use refine03')

    args = vars(parser.parse_args())    # vars returns a dictionary of the arguments

    print(args)

    
    
    
    if args['out_problem']:
        args['print_problem'] = True
    if args['out_domain']:
        args['print_domain'] = True




    #added for the second domain
    if args['out_problem2']:
        args['print_problem'] = True
    if args['out_domain2']:
        args['print_domain'] = True



    
    #added for unified domain/problem
    if args['out_unitop']:
        args['print_problem'] = True
    if args['out_unitod']:
        args['print_domain'] = True
    #print(args)  # just print the options that will be used


    # Parse the domain and problem given, build data structures
    domain  = PDDLParser.parse(args['domain-problem'][0])
    # print("==========> Domain parsed into memory....")

    problem = None
    if type(domain) is tuple:   # the first file contained both domain + problem
        problem = domain[1]
        domain = domain[0]


    if len(args['domain-problem']) == 2:    # two files have been given: domain and problem
        problem = PDDLParser.parse(args['domain-problem'][1])
        # print("==========> Problem parsed into memory....")
    
    
    #ipotizzo di voler passare 2 coppie di dominio-problema: domain, problem, domain2,problem2
    #if len(args['domain-problem']) == 4:    
        #problem = PDDLParser.parse(args['domain-problem'][1])
        #domain,domain2 = PDDLParser2.parse2(args['domain-problem'][0], args['domain-problem'][2]) levare
        #domain2=PDDLParser2.parse2(args['domain-problem'][0], args['domain-problem'][2])
        #problem2 = PDDLParser.parse(args['domain-problem'][3])
        # print("==========> Problem parsed into memory....")
    if len(args['domain-problem']) == 4:
        domain=PDDLParser.parse(args['domain-problem'][0])
        problem = PDDLParser.parse(args['domain-problem'][1])
        domain2=PDDLParser.parse(args['domain-problem'][2])
        problem2=PDDLParser.parse(args['domain-problem'][3])
        domain_unito=PDDLParser2.parse2(args['domain-problem'][0], args['domain-problem'][2],args['domain-problem'][1], args['domain-problem'][3])
        
        problem_unito = PDDLParser.parse(args['domain-problem'][3])
    
    


    if args['multi_tier_compilation']:
        if args['refine01']:
        # We extract the hierarchy from the problem definition just because it is easier
        # and is useful when compiling the domain
        
            domain_models_hierarchy,goal_statement = multi_tier_compilation_problem(problem,args['out_problem'])
            multi_tier_compilation_domain1(domain,domain_models_hierarchy,goal_statement,args['out_domain'])
        
        if args['basic']:
            domain_models_hierarchy,goal_statement = multi_tier_compilation_problem(problem,args['out_problem'])
            multi_tier_compilation_domain2(domain,domain_models_hierarchy,goal_statement,args['out_domain'])
        
        if args['downgrade']:
            domain_models_hierarchy,goal_statement = multi_tier_compilation_problem(problem,args['out_problem'])
            multi_tier_compilation_domain5(domain,domain_models_hierarchy,goal_statement,args['out_domain'])
        
        if args['upgrade']:
            domain_models_hierarchy,goal_statement = multi_tier_compilation_problem(problem,args['out_problem'])
            multi_tier_compilation_domain1(domain,domain_models_hierarchy,goal_statement,args['out_domain'])


        if args['refine02']:
            domain_models_hierarchy,goal_statement = multi_tier_compilation_problem(problem,args['out_problem'])
            multi_tier_compilation_domain3(domain,domain_models_hierarchy,goal_statement,args['out_domain'])
        
        if args['refine03']:
            domain_models_hierarchy,goal_statement = multi_tier_compilation_problem(problem,args['out_problem'])
            multi_tier_compilation_domain4(domain,domain_models_hierarchy,goal_statement,args['out_domain'])



    

    

    # test modifications to domain and problem
    if args['test_changes']:
        test_change_domain(domain)
        test_change_problem(problem)


    if args['print_domain']:
        if not args['out_domain']:
            print('=================================== TRANSLATED PDDL DOMAIN =================================== ')
            print(repr(domain))
            # print(domain)  # Pretty-printing
        else:
            with open(args['out_domain'], 'w') as f:
                print(repr(domain), file=f)
    




    if args['print_problem'] and not problem == None:
        if not args['out_problem']:
            print('=================================== TRANSLATED PDDL PROBLEM =================================== ')
            print(repr(problem))
            # print(problem)
        else:
            with open(args['out_problem'], 'w') as f:
                print(repr(problem), file=f)
    elif args['print_problem'] and problem == None:
        print("There was no problem found in the files provided")





    #adding part for the second couple of domain-problem

    if args['print_domain']:
        if not args['out_domain2']:
            print('=================================== TRANSLATED PDDL DOMAIN =================================== ')
            print(repr(domain2))
            # print(domain)  # Pretty-printing
        else:
            with open(args['out_domain2'], 'w') as f:
                print(repr(domain2), file=f)
    

    if args['print_problem'] and not problem2 == None:
        if not args['out_problem2']:
            print('=================================== TRANSLATED PDDL PROBLEM =================================== ')
            print(repr(problem2))
            # print(problem)
        else:
            with open(args['out_problem2'], 'w') as f:
                print(repr(problem2), file=f)
    elif args['print_problem'] and problem2 == None:
        print("There was no problem found in the files provided")

###adding a third part for a unified domain/problem
    if args['print_domain']:
        if not args['out_unitod']:
            print('=================================== TRANSLATED PDDL DOMAIN =================================== ')
            print(repr(domain_unito))
            # print(domain)  # Pretty-printing
        else:
            with open(args['out_unitod'], 'w') as f:
                print(repr(domain_unito), file=f)
    

    if args['print_problem'] and not problem_unito == None:
        if not args['out_unitop']:
            print('=================================== TRANSLATED PDDL PROBLEM =================================== ')
            print(repr(problem_unito))
            # print(problem)
        else:
            with open(args['out_unitop'], 'w') as f:
                print(repr(problem_unito), file=f)
    elif args['print_problem'] and problem_unito == None:
        print("There was no problem found in the files provided")






    

    





