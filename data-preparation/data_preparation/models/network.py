""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: network.py
authors: Elham Taghizadeh, Lucas Rebscher
date: 12/2023
description: The models defined for the network api
-----------------------------------------------------------------------------
"""

from enum import Enum
from uuid import uuid4
from pydantic import BaseModel


UnionValue = (
    str | bool | int | float | list[str] | list[bool] | list[int] | list[float] | None
)


class Position(BaseModel):
    x: float
    y: float


class ParameterValueType(Enum):
    STRING = "string"
    FLOAT = "float"
    INTEGER = "integer"
    BOOLEAN = "boolean"


class ModuleConfigParameter(BaseModel):
    """A single parameter of the module config."""

    id: str
    # name of param for display
    name: str #= None
    # type defines how user can interact with this param
    type: ParameterValueType #= None
    # the current value
    value: UnionValue = None
    # explanation what this param is about
    description: str #= None
    # whether `value` can be composed of multiple values
    multipleValues: bool = False
    # allowed values (e.g. column names)
    allowedValues: list[str] | None = None
    # whether `value` must be specified for this param
    required: bool = False


class ModuleConfig(BaseModel):
    parameters: dict[str, ModuleConfigParameter] = {}


class ModulePostBody(BaseModel):
    """Payload when creating a new module.

    - It requires a reference to the module blueprint/template
    """

    blueprint: str
    label: str
    position: Position


class SocketType(Enum):
    """
    The different supported types of sockets
    """
    FILE = "file"
    STRING = "string"
    BOOLEAN = "boolean"
    INTEGER = "integer"
    FLOAT = "float"
    ANY = "any"


class Socket(BaseModel):
    """
    The sockets of a node. A socket can be an input or an output.
    name (str): The name of the socket
    value (str): The value of the socket. depending on the type of the socket, it can be a file path, a string, a boolean, an integer or a float.
    type (SocketType): The type of the socket. The default value is SocketType.FILE
    """
    name: str
    value: UnionValue = None


class Module(BaseModel):
    """A module within a network."""

    id: str
    # label can be customized by user
    label: str
    # This API model is only used as internal representation.
    config: ModuleConfig | None = None
    # x/y position in the canvas
    position: Position
    # reference to the module's blueprint
    blueprint: str
    input_sockets: list[Socket]
    output_sockets: list[Socket]


class Connection(BaseModel):
    """
    A connection is from a node's output socket to another node's input socket.
    (sourceNode, sourceSocket) => (targetNode, targetSocket)
    """
    id: str = str(uuid4())
    sourceModule: str
    sourceSocket: str
    targetModule: str # The id of the target node
    targetSocket: str

class Network(BaseModel):
    """
    The network model.
    Holds all information
    - to display the network in the UI.
    - to trigger execution of any sub-graph in the network
    """
    id: str = str(uuid4())
    modules: list[Module]
    connections: list[Connection]


class ColumnType(str, Enum):
    """
    Column type determines how column is treated for further formatting & display
    """
    STRING = "string"
    BOOL = "bool"
    NUMBER = "number"


class Column(BaseModel):
    # name of a column in the table
    name: str
    # pandas dtype if it can be determined
    type: ColumnType


class TablePage(BaseModel):
    # columns filled with metadata
    columns: list[Column]
    # list of rows where each row is a dict of { column: value }
    data: list[dict[str, UnionValue]]


class RenderedVisualization(BaseModel):
    # image as base64 string
    image: str
