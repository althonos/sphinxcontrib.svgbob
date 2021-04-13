from hashlib import sha1
from typing import Any, Dict, List, Optional

from docutils.nodes import Element, General, Inline, Node
from docutils.parsers.rst import directives
from sphinx.builders import Builder
from sphinx.errors import SphinxError
from sphinx.ext.graphviz import align_spec, figure_wrapper
from sphinx.locale import __
from sphinx.util.docutils import SphinxDirective
from sphinx.util.i18n import search_image_for_language

from .node import svgbob


class SvgbobError(SphinxError):
    category = "Svgbob error"


class SvgbobDirective(SphinxDirective):
    """Directive to convert ASCII diagrams to SVG with Svgbob.
    """

    has_content = True
    required_arguments = 0
    optional_arguments = 3
    final_argument_whitespace = False
    # option_spec = {
    #     "filename": directives.unchanged,
    #     "type": type_spec,
    #     "format": format_spec,
    #     "align": align_spec,
    #     "caption": directives.unchanged,
    #     "class": directives.class_option,
    # }

    def run(self) -> List[Node]:
        document = self.state.document
        source: str = "\n".join(self.content)
        filename: Optional[str] = None
        diagram_type: Optional[str] = None
        output_format: Optional[str] = None

        # for argument in self.arguments:
        #     if argument in types:
        #         diagram_type = types.get(argument)
        #     elif argument in formats:
        #         output_format = argument
        #     else:
        #         filename = argument

        # if "filename" in self.options:
        #     if filename is not None:
        #         return [
        #             document.reporter.warning(
        #                 __(
        #                     "Kroki directive cannot have both filename option and "
        #                     "a filename argument"
        #                 ),
        #                 line=self.lineno,
        #             )
        #         ]
        #     filename = self.options["filename"]
        #
        # if source.strip() and filename is not None:
        #     return [
        #         document.reporter.warning(
        #             __(
        #                 "Kroki directive cannot have both content and "
        #                 "a filename argument"
        #             ),
        #             line=self.lineno,
        #         )
        #     ]

        # if filename is not None:
        #     argument = search_image_for_language(filename, self.env)
        #     rel_filename, filename = self.env.relfn2path(argument)
        #     self.env.note_dependency(rel_filename)
        #     try:
        #         with open(filename, encoding="utf-8") as fp:
        #             source = fp.read()
        #     except OSError:
        #         return [
        #             document.reporter.warning(
        #                 __(
        #                     "External kroki file %r not found or reading "
        #                     "it failed"
        #                 )
        #                 % filename,
        #                 line=self.lineno,
        #             )
        #         ]
        #
        # if not source.strip():
        #     return [
        #         document.reporter.warning(
        #             __(
        #                 "Ignoring kroki directive without content. It is necessary to specify "
        #                 "filename argument/option or content"
        #             ),
        #             line=self.lineno,
        #         )
        #     ]
        #
        # if "type" in self.options:
        #     if diagram_type is not None:
        #         return [
        #             document.reporter.warning(
        #                 __(
        #                     "Kroki directive cannot have both type option and "
        #                     "a type argument"
        #                 ),
        #                 line=self.lineno,
        #             )
        #         ]
        #     diagram_type = types.get(self.options["type"])
        #
        # if diagram_type is None:
        #     if filename is not None:
        #         suffix = Path(filename).suffix.lstrip(".")
        #         diagram_type = extension_type_map.get(
        #             suffix, types.get(suffix)
        #         )
        #
        #     if diagram_type is None:
        #         return [
        #             document.reporter.warning(
        #                 __("Kroki directive has to define diagram type."),
        #                 line=self.lineno,
        #             )
        #         ]
        #
        # if "format" in self.options:
        #     if output_format is not None:
        #         return [
        #             document.reporter.warning(
        #                 __(
        #                     "Kroki directive cannot have both format option and "
        #                     "a format argument"
        #                 ),
        #                 line=self.lineno,
        #             )
        #         ]
        #     output_format = self.options["format"]

        node = svgbob()

        node["type"] = diagram_type
        if output_format is not None:
            node["format"] = output_format
        node["code"] = source
        node["options"] = {"docname": self.env.docname}

        classes = ["svgbob"]
        node["classes"] = classes + self.options.get("class", [])
        if "align" in self.options:
            node["align"] = self.options["align"]

        return [node]

        # if "caption" not in self.options:
        #     self.add_name(node)
        #     return [node]
        # else:
        #     node["caption"] = self.options["caption"]
        #     figure = figure_wrapper(self, node, node["caption"])
        #     figure["classes"] = classes
        #     self.add_name(figure)
        #     return [figure]


# def render_kroki(
#     builder: Builder,
#     diagram_type: str,
#     diagram_source: str,
#     output_format: str,
#     prefix: str = "kroki",
# ) -> Path:
#     kroki_url: str = builder.config.kroki_url
#     payload: Dict[str, str] = {
#         "diagram_source": diagram_source,
#         "diagram_type": diagram_type,
#         "output_format": output_format,
#     }
#
#     hashkey = (str(kroki_url) + str(payload)).encode()
#     fname = "%s-%s.%s" % (prefix, sha1(hashkey).hexdigest(), output_format)
#     outfn = Path(builder.outdir).joinpath(builder.imagedir, fname)
#
#     if outfn.is_file():
#         return outfn
#
#     try:
#         outfn.parent.mkdir(parents=True, exist_ok=True)
#
#         response = requests.post(kroki_url, json=payload, stream=True)
#         response.raise_for_status()
#         with outfn.open(mode="wb") as f:
#             for chunk in response.iter_content(chunk_size=128):
#                 f.write(chunk)
#
#         return outfn
#     except requests.exceptions.RequestException as e:
#         raise KrokiError(__("kroki did not produce a diagram")) from e
#     except IOError as e:
#         raise KrokiError(
#             __("Unable to write diagram to file %r") % outfn
#         ) from e
