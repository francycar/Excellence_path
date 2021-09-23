# This file is part of pypddl-parser.

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


from ply import lex
from ply import yacc

from term import Term
from literal import Literal
from predicate import Predicate
from action import Action
from domain import Domain
from problem import Problem

tokens = (
    'NAME',
    'VARIABLE',
    'PROBABILITY',
    'LPAREN',
    'RPAREN',
    'HYPHEN',
    'EQUALS',
    'DEFINE_KEY',
    'DOMAIN_KEY',
    'REQUIREMENTS_KEY',
    'STRIPS_KEY',
    'EQUALITY_KEY',
    'TYPING_KEY',
    'PROBABILISTIC_EFFECTS_KEY',
    'TYPES_KEY',
    'CONSTANTS_KEY',
    'PREDICATES_KEY',
    'ACTION_KEY',
    'PARAMETERS_KEY',
    'PRECONDITION_KEY',
    'EFFECT_KEY',
    'AND_KEY',
    'NOT_KEY',
    'ONEOF_KEY',
    'PROBABILISTIC_KEY',
    'PROBLEM_KEY',
    'OBJECTS_KEY',
    'INIT_KEY',
    'GOAL_KEY',
    'WHEN_KEY',
    'OR_KEY'
)

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_HYPHEN = r'\-'
t_EQUALS = r'='

t_ignore = ' \t'

reserved = {
    'define': 'DEFINE_KEY',
    'domain': 'DOMAIN_KEY',
    ':requirements': 'REQUIREMENTS_KEY',
    ':strips': 'STRIPS_KEY',
    ':equality': 'EQUALITY_KEY',
    ':typing': 'TYPING_KEY',
    ':probabilistic-effects': 'PROBABILISTIC_EFFECTS_KEY',
    ':types': 'TYPES_KEY',
    ':predicates': 'PREDICATES_KEY',
    ':action': 'ACTION_KEY',
    ':parameters': 'PARAMETERS_KEY',
    ':precondition': 'PRECONDITION_KEY',
    ':effect': 'EFFECT_KEY',
    'and': 'AND_KEY',
    'not': 'NOT_KEY',
    'oneof': 'ONEOF_KEY',
    'when': 'WHEN_KEY',
    'or': 'OR_KEY',
    'probabilistic': 'PROBABILISTIC_KEY',
    'problem': 'PROBLEM_KEY',
    ':domain': 'DOMAIN_KEY',
    ':objects': 'OBJECTS_KEY',
    ':constants': 'CONSTANTS_KEY',
    ':init': 'INIT_KEY',
    ':goal': 'GOAL_KEY'
}


def t_KEYWORD(t):
    r':?[a-zA-z_][a-zA-Z_0-9\-]*'
    t.type = reserved.get(t.value, 'NAME')
    return t


def t_NAME(t):
    r'[a-zA-z_][a-zA-Z_0-9\-]*'
    return t


def t_VARIABLE(t):
    r'\?[a-zA-z_][a-zA-Z_0-9\-]*'
    return t


def t_PROBABILITY(t):
    r'[0-1]\.\d+'
    t.value = float(t.value)
    return t


def t_newline(t):
    r'\n+'
    t.lineno += len(t.value)


def t_error(t):
    print("Error: illegal character '{0}'".format(t.value[0]))
    t.lexer.skip(1)


# build the lexer
lex.lex()


def p_pddl(p):
    '''pddl : domain
            | problem
            | domain problem'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = (p[1], p[2])


###################################################3
# Rules for PLANNING DOMAIN
###################################################3
def p_domain(p):
    '''domain : LPAREN DEFINE_KEY domain_def require_def types_def constants_def predicates_def action_def_lst RPAREN
              | LPAREN DEFINE_KEY domain_def require_def types_def predicates_def action_def_lst RPAREN
              | LPAREN DEFINE_KEY domain_def require_def constants_def predicates_def action_def_lst RPAREN
              | LPAREN DEFINE_KEY domain_def require_def predicates_def action_def_lst RPAREN'''
    if len(p) == 10:  # both types and constants are given
        p[0] = Domain(p[3], p[4], p[5][1], p[6][1], p[7], p[8])  # both :types and :constants
    elif len(p) == 9:
        if p[5][0] == "types":
            p[0] = Domain(p[3], p[4], p[5][1], {}, p[6], p[7])  # :types but no constants
        elif p[5][0] == "constants":
            p[0] = Domain(p[3], p[4], {}, p[5][1], p[6], p[7])  # no :types, but :constants
    elif len(p) == 8:
        p[0] = Domain(p[3], p[4], {}, {}, p[5], p[6])  # no :constants or :types


def p_domain_def(p):
    '''domain_def : LPAREN DOMAIN_KEY NAME RPAREN'''
    p[0] = p[3]


def p_require_def(p):
    '''require_def : LPAREN REQUIREMENTS_KEY require_key_lst RPAREN'''
    p[0] = p[3]


def p_require_key_lst(p):
    '''require_key_lst : require_key require_key_lst
                       | require_key'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = [p[1]] + p[2]


def p_require_key(p):
    '''require_key : STRIPS_KEY
                   | EQUALITY_KEY
                   | TYPING_KEY
                   | PROBABILISTIC_EFFECTS_KEY'''
    p[0] = str(p[1])


def p_types_def(p):
    '''types_def : LPAREN TYPES_KEY typed_names_lst RPAREN'''
    p[0] = ("types", p[3])


def p_constants_def(p):
    '''constants_def : LPAREN CONSTANTS_KEY typed_names_lst RPAREN'''
    p[0] = ("constants", p[3])


# Used for processing :types and :constants
#   list of names, possibly typed using hyphen -
def p_typed_names_lst(p):
    '''typed_names_lst : names_lst HYPHEN type typed_names_lst
                       | names_lst HYPHEN type
                       | names_lst'''
    if len(p) == 2:
        p[0] = dict({'': p[1]})
    elif len(p) == 4:
        p[0] = dict({p[3]: p[1]})
    elif len(p) == 5:
        if p[3] in p[4]:
            p[4][p[3]] = p[4][p[3]] + p[1]
        else:
            p[4][p[3]] = p[1]
        p[0] = p[4]  # p[4] is already a dictionary, add one entry more


def p_predicates_def(p):
    '''predicates_def : LPAREN PREDICATES_KEY predicate_def_lst RPAREN'''
    p[0] = p[3]


def p_predicate_def_lst(p):
    '''predicate_def_lst : predicate_def predicate_def_lst
                         | predicate_def'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = [p[1]] + p[2]


def p_predicate_def(p):
    '''predicate_def : LPAREN NAME typed_variables_lst RPAREN
                     | LPAREN NAME variables_lst RPAREN
                     | LPAREN NAME RPAREN'''
    if len(p) == 4:
        p[0] = Predicate(p[2])
    elif len(p) == 5:
        p[0] = Predicate(p[2], p[3])


def p_action_def_lst(p):
    '''action_def_lst : action_def action_def_lst
                      | action_def'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = [p[1]] + p[2]


def p_action_def(p):
    '''action_def : LPAREN ACTION_KEY NAME parameters_def action_def_body RPAREN'''
    p[0] = Action(p[3], p[4], p[5][0], p[5][1])


def p_parameters_def(p):
    '''parameters_def : PARAMETERS_KEY LPAREN typed_variables_lst RPAREN
                      | PARAMETERS_KEY LPAREN variables_lst RPAREN
                      | PARAMETERS_KEY LPAREN RPAREN'''
    if len(p) == 4:
        p[0] = []
    elif len(p) == 5:
        p[0] = p[3]


def p_action_def_body(p):
    '''action_def_body : precond_def effects_def'''
    p[0] = (p[1], p[2])


def p_precond_def(p):
    '''precond_def : PRECONDITION_KEY LPAREN AND_KEY literals_lst RPAREN

                   | PRECONDITION_KEY literal'''
    if len(p) == 3:
        p[0] = [p[2]]
    elif len(p) == 6:
        p[0] = p[4]


def p_effects_def(p):
    '''effects_def : EFFECT_KEY effect_body'''
    if len(p) == 3:
        p[0] = p[2]


def p_effect_body(p):
    '''effect_body : LPAREN NAME unlabeled_effect RPAREN
                    | effect_body LPAREN NAME unlabeled_effect RPAREN
                    | unlabeled_effect'''
    if len(p) == 5:
        p[0] = [(p[2], p[3])]
    elif len(p) == 6:
        p[0] = p[1] + [(p[3], p[4])]
    elif len(p) == 2:
        p[0] = p[1]


def p_unlabeled_effect(p):
    '''unlabeled_effect : LPAREN ONEOF_KEY effect_body RPAREN
                        | deterministic_effect unlabeled_effect
                        | deterministic_effect'''
    if len(p) == 5:
        p[0] = p[3]
    elif len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = [p[1]] + p[2]


def p_deterministic_effect(p):
    '''deterministic_effect : LPAREN AND_KEY effects_lst RPAREN
                            | effects_lst'''
    if len(p) == 2:
        p[0] = p[1]  # effect is just on literal, no AND
    elif len(p) == 5:
        p[0] = p[3]  # effect description has an AND


def p_when_effects(p):
    '''when_effects : when_if when_then '''
    p[0] = [p[1],
            p[2]]  # it is a list, with the element in [0] being the conditions and the element in [1] being the effects


def p_when_if(p):
    '''when_if : simple_effect
                | LPAREN AND_KEY simple_effects_lst RPAREN'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 5:
        p[0] = p[3]


def p_when_then(p):
    '''when_then : simple_effect
                | LPAREN AND_KEY simple_effects_lst RPAREN'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 5:
        p[0] = p[3]


def p_effects_lst(p):
    '''effects_lst : effect effects_lst
                   | effect'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = [p[1]] + p[2]


def p_simple_effects_lst(p):
    '''simple_effects_lst : simple_effect simple_effects_lst
                   | simple_effect'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = [p[1]] + p[2]


def p_effect(p):
    '''effect : literal
              | LPAREN PROBABILISTIC_KEY PROBABILITY literal RPAREN
              | LPAREN WHEN_KEY when_effects RPAREN'''
    if len(p) == 2:
        p[0] = (1.0, p[1])
    elif len(p) == 6:
        p[0] = (p[3], p[4])
    elif len(p) == 5:
        p[0] = p[3]


def p_simple_effect(p):
    '''simple_effect : literal'''
    if len(p) == 2:
        p[0] = (1.0, p[1])


def p_literals_lst(p):
    '''literals_lst : literal literals_lst
                    | literal

                    | or_literal literals_lst
                    | or_literal

                    | and_literal literals_lst
                    | and_literal'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = [p[1]] + p[2]

def p_and_literal(p):
    '''and_literal : LPAREN AND_KEY literals_lst RPAREN
                   | literal'''
    if len(p) == 5:
        p[0] = p[3]
    elif len(p) == 2:
        p[0] = p[1]


def p_or_literal(p):
    '''or_literal : LPAREN OR_KEY literals_lst RPAREN
                  | literal'''
    if len(p) == 5:
        p[0] = p[3]
    elif len(p) == 2:
        p[0] = p[1]

def p_literal(p):
    '''literal : LPAREN NOT_KEY predicate RPAREN
               | predicate'''
    if len(p) == 2:
        p[0] = Literal.positive(p[1])
    elif len(p) == 5:
        p[0] = Literal.negative(p[3])


def p_ground_predicates_lst(p):
    '''ground_predicates_lst : ground_predicate ground_predicates_lst
                             | ground_predicate'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = [p[1]] + p[2]


def p_predicate(p):
    '''predicate : LPAREN NAME variables_lst RPAREN
                 | LPAREN EQUALS VARIABLE VARIABLE RPAREN
                 | LPAREN NAME RPAREN
                 | LPAREN NAME constants_lst RPAREN'''
    if len(p) == 4:
        p[0] = Predicate(p[2])
    elif len(p) == 5:
        p[0] = Predicate(p[2], p[3])
    elif len(p) == 6:
        p[0] = Predicate('=', [p[3], p[4]])


def p_ground_predicate(p):
    '''ground_predicate : LPAREN NAME constants_lst RPAREN
                        | LPAREN NAME RPAREN'''
    if len(p) == 4:
        p[0] = Predicate(p[2])
    elif len(p) == 5:
        p[0] = Predicate(p[2], p[3])


def p_typed_constants_lst(p):
    '''typed_constants_lst : constants_lst HYPHEN type typed_constants_lst
                           | constants_lst HYPHEN type'''
    if len(p) == 4:
        p[0] = [Term.constant(value, p[3]) for value in p[1]]
    elif len(p) == 5:
        p[0] = [Term.constant(value, p[3]) for value in p[1]] + p[4]


def p_typed_variables_lst(p):
    '''typed_variables_lst : variables_lst HYPHEN type typed_variables_lst
                           | variables_lst HYPHEN type'''
    if len(p) == 4:
        p[0] = [Term.variable(name, p[3]) for name in p[1]]
    elif len(p) == 5:
        p[0] = [Term.variable(name, p[3]) for name in p[1]] + p[4]


def p_constants_lst(p):
    '''constants_lst : constant constants_lst
                     | constant'''
    if len(p) == 2:
        p[0] = [Term.constant(p[1])]
    elif len(p) == 3:
        p[0] = [Term.constant(p[1])] + p[2]


def p_variables_lst(p):
    '''variables_lst : variable variables_lst
                     | variable'''
    if len(p) == 2:
        p[0] = [Term.variable(p[1])]
    elif len(p) == 3:
        p[0] = [Term.variable(p[1])] + p[2]


def p_names_lst(p):
    '''names_lst : NAME names_lst
                 | NAME'''
    if len(p) == 1:
        p[0] = []
    elif len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = [p[1]] + p[2]


def p_type(p):
    '''type : NAME'''
    p[0] = p[1]


def p_constant(p):
    '''constant : NAME'''
    p[0] = p[1]


def p_variable(p):
    '''variable : VARIABLE'''
    p[0] = p[1]


###################################################3
# Rules for PLANNING PROBLEM
###################################################3
def p_problem(p):
    '''problem : plan_problem'''
    p[0] = p[1]


def p_plan_problem(p):
    '''plan_problem : LPAREN DEFINE_KEY plan_problem_def domain_def objects_def init_def goal_def RPAREN
                    | LPAREN DEFINE_KEY plan_problem_def domain_def init_def goal_def RPAREN'''
    if len(p) == 9:
        p[0] = Problem(p[3], p[4], p[5], p[6], p[7])
    elif len(p) == 8:
        p[0] = Problem(p[3], p[4], {}, p[5], p[6])


def p_plan_problem_def(p):
    '''plan_problem_def : LPAREN PROBLEM_KEY NAME RPAREN'''
    p[0] = p[3]


def p_objects_def(p):
    '''objects_def : LPAREN OBJECTS_KEY typed_constants_lst RPAREN
                   | LPAREN OBJECTS_KEY constants_lst RPAREN'''
    p[0] = p[3]


def p_init_def(p):
    '''init_def : LPAREN INIT_KEY LPAREN AND_KEY ground_predicates_lst RPAREN RPAREN
                | LPAREN INIT_KEY ground_predicates_lst RPAREN'''
    if len(p) == 5:
        p[0] = p[3]
    elif len(p) == 8:
        p[0] = p[5]


def p_goal_def(p):
    '''goal_def : LPAREN GOAL_KEY LPAREN AND_KEY literals_lst RPAREN RPAREN
                | LPAREN GOAL_KEY literal RPAREN
                | LPAREN GOAL_KEY LPAREN ONEOF_KEY effect_body RPAREN RPAREN'''
    if len(p) == 8:
        p[0] = p[5]
    elif len(p) == 5:
        p[0] = [p[3]]
    elif len(p) == 14:
        p[0] = (p[6], p[9])


def p_error(p):
    print("Error: syntax error when parsing '{}'".format(p))


# build parser
yacc.yacc()


class PDDLParser(object):

    @classmethod
    def parse(cls, filename):
        data = cls.__read_input(filename)
        return yacc.parse(data)

    @classmethod
    def __read_input(cls, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            data = ''
            for line in file:
                line = line.rstrip().lower()
                line = cls.__strip_comments(line)
                data += '\n' + line
        return data

    @classmethod
    def __strip_comments(cls, line):
        pos = line.find(';')
        if pos != -1:
            line = line[:pos]
        return line


class PDDLParser2(object):

    @classmethod
    def parse2(cls, filename, filename1, filename2, filename3):
        data = cls.__read_input2(filename)
        data1 = cls.__read_input2(filename1)

        data2 = cls.__read_input2(filename2)
        data3 = cls.__read_input2(filename3)
        print(type(data))
        parsato = yacc.parse(data)

        parsato1 = yacc.parse(data1)

        parsato2 = yacc.parse(data2)
        parsato3 = yacc.parse(data3)

        unified_domain = cls.__create_labelled_domain(parsato, parsato1)

        unified_problem = cls.__create_labelled_problem(parsato2, parsato3)
        return unified_domain, unified_problem

    @classmethod
    def __read_input2(cls, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            data = ''
            for line in file:
                line = line.rstrip().lower()
                line = cls.__strip_comments2(line)
                data += '\n' + line

        return data

    @classmethod
    def __strip_comments2(cls, line):
        pos = line.find(';')
        if pos != -1:
            line = line[:pos]
        return line

    @classmethod
    # funzione per creare il problema labelled unificato
    def __create_labelled_problem(cls, problem, problem1):
        with open('unified_pb.pddl', 'w') as f:
            print(repr(problem), file=f)

        data_pb = cls.__read_input2('unified_pb.pddl')

        parsato_pb = yacc.parse(data_pb)

        goal2 = ('d2', problem.goal)

        goal1 = ('d1', problem1.goal)

        labelled_goal = [goal2, goal1]

        print(labelled_goal)

        problem.goal = labelled_goal

        with open('unified_pb.pddl', 'w') as f:
            print(repr(problem), file=f)

    @classmethod
    # funzione per creare il dominio labelled unificato
    def __create_labelled_domain(cls, domain, domain1):
        with open('unified_dom.pddl', 'w') as f:
            print(repr(domain), file=f)

        data_new = cls.__read_input2('unified_dom.pddl')
        print(type(data_new))
        parsato_newd = yacc.parse(data_new)
        print('tipo', type(parsato_newd))

        for (action, action1) in zip(domain.operators, domain1.operators):
            if (action.name == action1.name):
                tupla_d1 = ('d1', action.effects)

                tupla_d2 = ('d2', action1.effects)

                lista_eff = [tupla_d2, tupla_d1]
                print(lista_eff)

                action_list = action.effects

                print('action:list->dopo', action_list)

                print(type(action_list[0][0][1]))

                action_list += action1.effects

                # parsato_newd.add_action(action.name,[], action.precond, action_list)

                parsato_newd.add_action(action.name, [], action.precond, lista_eff)

        lista_ = parsato_newd.operators

        # elimino le azioni vecchie senza il oneof estratte dai domini separati  e inserisco le nuove compatte con il oneof
        for i in range(len(domain1.operators)):
            lista_.remove(parsato_newd.operators[i])

        parsato_newd.operators = lista_

        with open('unified_dom.pddl', 'w') as f:
            print(repr(parsato_newd), file=f)


class PDDLParser3(object):

    @classmethod
    def parse3(cls, domains_list, problems_list, unified_domain, unified_problem):
        # unified_domain= cls.__create_labelled_domain_extended(domains_list)
        # unified_problem= cls.__create_labelled_problem_extended(problems_list)
        cls.__create_labelled_domain_extended(domains_list, unified_domain)
        cls.__create_labelled_problem_extended(problems_list, unified_problem)
        # return unified_domain,unified_problem

    @classmethod
    def __read_input3(cls, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            data = ''
            for line in file:
                line = line.rstrip().lower()
                line = cls.__strip_comments3(line)
                data += '\n' + line

        return data

    @classmethod
    def __strip_comments3(cls, line):
        pos = line.find(';')
        if pos != -1:
            line = line[:pos]
        return line

    @classmethod
    # funzione per creare il dominio labelled unificato
    def __create_labelled_domain_extended(cls, domains_list, unified_domain):
        """Create labeled domain."""
        data1 = cls.__read_input3(domains_list[0])
        head_domain = yacc.parse(data1)

        original_operators=head_domain.operators

        stand_actions=0
        for m in range(len( original_operators)):
            if ('trans' not  in original_operators[m].name):
                stand_actions=stand_actions+1
        print('Contatore',stand_actions)


        #with open(unified_domain, 'w') as f:
            #f.write(repr(head_domain))
            #f.close()
        #print('tipo unified', type(unified_domain))
            # print(repr(head_domain), file=f)

        # perché parsi nuovamente??
        #data_new = cls.__read_input3(unified_domain)
        #print(type(data_new))
        #parsato_newd = yacc.parse(data_new)
        #print('tipo', type(parsato_newd))
        parsato_newd=head_domain

        domains_list1 = []

        for i in range(len(domains_list)):
            if i != 0:
                domains_list1.append(domains_list[i])

        for i in range(len(domains_list1)):
            data_i = cls.__read_input3(domains_list1[i])
            domain_i = yacc.parse(data_i)
            print('domain_i_operators', domain_i.operators)

            #if (len(domain_i.operators) == len(head_domain.operators)):
            print('len operators',len(domain_i.operators))
            for j in range(len(domain_i.operators)):
                eff_list = []
                if (('trans' not in domain_i.operators[j].name) and ('trans' not in head_domain.operators[j].name) and
                        (domain_i.operators[j].name == head_domain.operators[j].name)):

                    d_tuple1 = ('d' + str(1), head_domain.operators[j].effects)
                    eff_list.append(d_tuple1)

                    for k in range(len(domains_list1)):
                        d_tuple = ('d' + str(k + 2), domain_i.operators[j].effects)
                        eff_list.append(d_tuple)

                    def Reverse(lst):
                        return [ele for ele in reversed(lst)]

                    print(Reverse(eff_list))

                    eff_list_reversed = Reverse(eff_list)








                    parsato_newd.add_action(domain_i.operators[j].name, domain_i.operators[j].params, domain_i.operators[j].precond,
                                                eff_list_reversed)









                if ('trans' in domain_i.operators[j].name):


                    parsato_newd.add_action(domain_i.operators[j].name + str(i+1+1), domain_i.operators[j].params,domain_i.operators[j].precond, domain_i.operators[j].effects)

        for k in range(len(original_operators)):
            if ('trans' in original_operators[k].name):
                parsato_newd.add_action(original_operators[k].name + str(1), original_operators[k].params, original_operators[k].precond,
                                        original_operators[k].effects)

        lista_ = parsato_newd.operators

        # rimuovo ultimo elemento perchè è di ripetizione



        index=len(original_operators)


        print('INDEX',index)

        print('PRIMA',lista_)


        action_list = []

        for i in range(len(original_operators)):
            #if('trans' not in original_operators[i].name):
            action_list.append(original_operators[i])
        print('ACTION LIST_', action_list)
        print('LIDTA base_', lista_)

        index_of_standard_action=len(action_list)
        print('standard',index_of_standard_action)

        lista1_ = []
        for h in range(len(lista_)):
            if (h  not in range(index_of_standard_action)):
                lista1_.append(lista_[h])

        print('lista1', lista1_)




        lista2_=[]
        for n in range(stand_actions):
            lista2_.append(lista1_[n])


        lista_trans=[]
        for m in range(len(lista1_)):
            if('trans' in lista1_[m].name):
                lista_trans.append(lista1_[m])



        final_list=lista2_+lista_trans






        parsato_newd.operators = final_list

        print('actions',parsato_newd.operators)

        with open(unified_domain, 'w') as f:
            print(repr(parsato_newd), file=f)

    @classmethod
    # funzione per creare il problema labelled unificato
    def __create_labelled_problem_extended(cls, problems_list, unified_problem):

        # with open('unified_pb.pddl', 'w') as f:
        with open(unified_problem, 'w') as f:
            problem_data1 = cls.__read_input3(problems_list[0])
            problem1 = yacc.parse(problem_data1)

            print(repr(problem1), file=f)

            labelled_goal = []
            print('len pb list', problems_list)
            for i in range(len(problems_list)):
                data_i = cls.__read_input3(problems_list[i])
                parse_i = yacc.parse(data_i)

                print('DATAi', parse_i)

                tupla = (1.0, parse_i.goal[0])
                tupla_list = [tupla]
                print('this is tupla', tupla_list)

                goal_ = ('d' + str(i + 1), [tupla_list])
                labelled_goal.append(goal_)

            print('printa labelled', labelled_goal)

            def Reverse(lst):
                return [ele for ele in reversed(lst)]

            labelled_goal_reversed = Reverse(labelled_goal)

            problem1.goal = labelled_goal_reversed

            print('stampa problem1.goal', problem1.goal)

        with open(unified_problem, 'w') as unified_problem:
            print(Problem.oneof_repr(problem1), file=unified_problem)
