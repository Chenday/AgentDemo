from tools.ToolExecutor import ToolExecutor

from . import serpApi


ToolExecutor.registerTool("Search", serpApi.description, serpApi.search)


