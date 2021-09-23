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

"""Main entrypoint for the Multi-Tier Planning for LTLf/PLTLf Goals CLI tool."""
import logging

logging.basicConfig(format='%(asctime)s:%(levelname)s %(message)s', level=logging.DEBUG)

from pddlparser import PDDLParser3
from mtp import multi_tier_compilation_problem, multi_tier_compilation_domain1, multi_tier_compilation_domain2
import click

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    "-q",
    "--quiet",
    is_flag=True,
    help="Don't print anything."
)
@click.option(
    "-d",
    "--domains",
    required=True,
    help="Path to domains file.",
    type=click.Path(exists=True, readable=True),
)
@click.option(
    "-p",
    "--problems",
    required=True,
    help="Path to problems file.",
    type=click.Path(exists=True, readable=True),
)
@click.option(
    "--refine",
    is_flag=True,
    default=False,
    show_default=True,
)
@click.option(
    "--basic",
    is_flag=True,
    default=False,
    show_default=True,
)
@click.option(
    "-outd",
    "--out-domain",
    default="./out-domain.pddl",
    help="Path to PDDL file to store the new domain.",
    type=click.Path(dir_okay=False),
)
@click.option(
    "-outp",
    "--out-problem",
    default="./out-problem.pddl",
    help="Path to PDDL file to store the new problem.",
    type=click.Path(dir_okay=False),
)
@click.option(
    "-outmultid",
    "--out-multidomain",
    default="./out-multidomain.pddl",
    help="Path to PDDL file to store the new multi tier domain.",
    type=click.Path(dir_okay=False),
)
@click.option(
    "-outmultip",
    "--out-multiproblem",
    default="./out-multiproblem.pddl",
    help="Path to PDDL file to store the new multi tier problem.",
    type=click.Path(dir_okay=False),
)
def cli(quiet, domains, problems, refine, basic, out_domain, out_problem, out_multidomain, out_multiproblem):
    """Multi-Tier Planning for LTLf/PLTLf Goals."""  # noqa
    try:
        with open(domains, "r") as d:
            domain_paths = d.readlines()
            domain_paths = [x.strip() for x in domain_paths]
        with open(problems, "r") as p:
            problem_paths = p.readlines()
            problem_paths = [x.strip() for x in problem_paths]
        if len(domain_paths) != len(problem_paths):
            raise IOError(
                "[ERROR]: Same number of domains and problems expected."
            )
    except Exception:
        raise IOError(
            "[ERROR]: Something wrong occurred while parsing domains and problems."
        )

    if not quiet:
        logging.debug(f"Paths parsed, number of domains/problems: {len(domain_paths)}")
    # il comando che segue va integrato!
    # unified_domain, unified_problem = PDDLParser3.parse3(domain_paths, problem_paths,out_domain,out_problem)
    PDDLParser3.parse3(domain_paths, problem_paths, out_domain, out_problem)
    if not quiet:
        logging.debug("Domains and problems unified")

    domain_models_hierarchy, goal_statement = multi_tier_compilation_problem(out_problem, out_multiproblem)
    if refine:
        if not quiet:
            logging.debug("Refine flag turned on!")
        # i comandi che seguono vanno modificati usando unified_domain e unified_problem!
        multi_tier_compilation_domain1(out_domain, domain_models_hierarchy, goal_statement, out_multidomain)
    if basic:
        multi_tier_compilation_domain2(out_domain, domain_models_hierarchy, goal_statement, out_multidomain)

    # lo snippet sotto è per la stampa del risultato!
    # try:
    # with open(out_domain, "w+") as dom:
    # dom.write(str(unified_domain))
    # with open(out_problem, "w+") as prob:
    # prob.write(str(unified_problem))
    # except Exception:
    # raise IOError(
    # "[ERROR]: Something wrong occurred while writing new problem and domain."
    # )


if __name__ == "__main__":
    cli()  # pragma: no cover
