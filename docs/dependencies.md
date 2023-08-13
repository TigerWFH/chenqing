# dependencies

## Tkinter 模块

> tkinter 包 ("Tk 接口") 是针对 Tcl/Tk GUI 工具包的标准 Python 接口。 Tk 和 tkinter 在大多数 Unix 平台，包括 macOS，以及 Windows 系统上均可使用。
>
> 在命令行执行 python -m tkinter，应会弹出一个简单的 Tk 界面窗口， 表明 tkinter 包已安装完成
>
> Tcl/Tk 不是只有单个库，而是由几个不同的模块组成的

> - `Tcl` 是一种动态解释型编程语言，正如 Python 一样。尽管它可作为一种通用的编程语言单独使用，但最常见的用法还是作为脚本引擎或 Tk 工具包的接口嵌入到 C 程序中。Tcl 库有一个 C 接口，用于创建和管理一个或多个 Tcl 解释器实例，并在这些实例中运行 Tcl 命令和脚本，添加用 Tcl 或 C 语言实现的自定义命令。

> - `Tk` is a Tcl package implemented in C that adds custom commands to create and manipulate GUI widgets.
> - 带有主题的 `Tk（Ttk）`是较新加入的 Tk 部件。在内部，Tk 和 Ttk 使用下层操作系统的工具库，例如在 Unix/X11 上是 Xlib，在 macOS 上是 Cocoa，在 Windows 上是 GDI。
> - 对 Tkinter 的支持分布在多个模块中。 大多数应用程序将需要主模块 `tkinter`，以及 `tkinter.ttk` 模块，后者提供了带主题的现代部件集及相应的 API:

## Apis

> class tkinter.Tk(screenName=None, baseName=None, className='Tk', useTk=True, sync=False, use=None)
