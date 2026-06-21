# Effective Go

> 高效 Go

**Note:** This document was written for Go's release in 2009 and is not actively updated. While it remains a good guide for using the core language, it does not cover significant changes to the language (generics), ecosystem (modules), or libraries added since. See [issue 28782](https://go.dev/issue/28782) for context. For a complete list of changes, see the [release notes](https://go.dev/doc/devel/release).

> **说明：** 本文写于 Go 2009 年发布之初，目前已经不再主动更新。它仍然是理解 Go 核心语言用法的好指南，但没有覆盖后来加入的重要变化，包括语言层面的泛型、生态层面的模块，以及新增的库。相关背景可见 [issue 28782](https://go.dev/issue/28782)。完整变更列表请参阅 [release notes](https://go.dev/doc/devel/release)。

## Introduction

> 引言

Go is an open-source programming language that focuses on simplicity, reliability, and efficiency, specifically designed to make it easy to build software at scale. Although it borrows ideas from existing languages, it has unusual properties that make effective Go programs different in character from programs written in its relatives. A straightforward translation of a C++ or Java program into Go is unlikely to produce a satisfactory result—Java programs are written in Java, not Go. On the other hand, thinking about the problem from a Go perspective could produce a successful but quite different program. In other words, to write Go well, it's important to understand its properties and idioms. It's also important to know the established conventions for programming in Go, such as naming, formatting, program construction, and so on, so that programs you write will be easy for other Go programmers to understand.

> Go 是一门开源编程语言，强调简单、可靠和高效，目标是让大规模软件构建变得更容易。它借鉴了已有语言的许多思想，但也有自己的独特性质，因此写得好的 Go 程序，风格会明显不同于那些相近语言写出的程序。把 C++ 或 Java 程序直接翻译成 Go，通常不会得到理想结果。Java 程序应该按 Java 的方式写，Go 程序也应该按 Go 的方式思考。换句话说，想写好 Go，就要理解它的特性和惯用法，也要熟悉 Go 社区约定俗成的规则，比如命名、格式、程序组织等。这样写出来的程序，其他 Go 程序员才容易理解。

This document gives tips for writing clear, idiomatic Go code. It augments the [language specification](https://go.dev/ref/spec), the [Tour of Go](https://go.dev/tour/), and [How to Write Go Code](https://go.dev/doc/code.html), all of which you should read first.

> 本文提供了一些建议，帮助你写出清晰、符合 Go 习惯的代码。它是对 [language specification](https://go.dev/ref/spec)、[Tour of Go](https://go.dev/tour/) 和 [How to Write Go Code](https://go.dev/doc/code.html) 的补充；这些文档都值得先读。

### Examples

> 示例

The [Go package sources](https://go.dev/src/) are intended to serve not only as the core library but also as examples of how to use the language. Moreover, many of the packages contain working, self-contained executable examples you can run directly from the [go.dev](https://go.dev/) web site, such as [this one](https://go.dev/pkg/strings/#example-Map) (if necessary, click on the word "Example" to open it up). If you have a question about how to approach a problem or how something might be implemented, the documentation, code and examples in the library can provide answers, ideas and background.

> [Go 包源码](https://go.dev/src/) 不只是核心库，也是一组展示语言用法的示例。许多包还带有完整、可运行的独立示例，可以直接在 [go.dev](https://go.dev/) 网站上运行，例如 [这个示例](https://go.dev/pkg/strings/#example-Map)；如果需要，点击 “Example” 展开即可。如果你不确定某个问题该怎么处理，或者某个功能该如何实现，标准库中的文档、代码和示例往往能提供答案、思路和背景。

## Formatting

> 格式化

Formatting issues are the most contentious but the least consequential. People can adapt to different formatting styles but it's better if they don't have to, and less time is devoted to the topic if everyone adheres to the same style. The problem is how to approach this Utopia without a long prescriptive style guide.

> 格式问题最容易引发争论，但通常也最不影响程序本身。人们可以适应不同的格式风格，但如果大家不必适应就更好；如果所有人都遵循同一种风格，花在格式讨论上的时间也会更少。问题是，怎样在不写一长篇规定式风格指南的情况下接近这种理想状态。

With Go we take an unusual approach and let the machine take care of most formatting issues. The `gofmt` program (also available as `go fmt`, which operates at the package level rather than source file level) reads a Go program and emits the source in a standard style of indentation and vertical alignment, retaining and if necessary reformatting comments. If you want to know how to handle some new layout situation, run `gofmt`; if the answer doesn't seem right, rearrange your program (or file a bug about `gofmt`), don't work around it.

> Go 采用了不太寻常的做法：让机器处理大部分格式问题。`gofmt` 程序会读取 Go 源码，并按标准风格输出，包括缩进、纵向对齐、保留注释以及必要时重新排版注释。`go fmt` 也可用，它作用于包级别，而不是单个源码文件。如果你不确定某种布局该怎么写，运行 `gofmt` 看结果即可；如果结果看起来不对，就调整程序结构，或者提交 `gofmt` 的问题，不要绕开它另搞一套。

As an example, there's no need to spend time lining up the comments on the fields of a structure. `Gofmt` will do that for you. Given the declaration

> 举个例子，你不需要花时间手动对齐结构体字段后面的注释，`gofmt` 会替你完成。假设有下面的声明：

    type T struct {
        name string // name of the object
        value int // its value
    }

`gofmt` will line up the columns:

> `gofmt` 会把列对齐：

    type T struct {
        name    string // name of the object
        value   int    // its value
    }

All Go code in the standard packages has been formatted with `gofmt`.

> 标准库中的所有 Go 代码都经过了 `gofmt` 格式化。

Some formatting details remain. Very briefly:

> 还有少量格式细节需要说明。简要来说：

Indentation  
We use tabs for indentation and `gofmt` emits them by default. Use spaces only if you must.

> 缩进
> 使用制表符缩进，`gofmt` 默认也会输出制表符。只有在确有必要时才使用空格。

Line length  
Go has no line length limit. Don't worry about overflowing a punched card. If a line feels too long, wrap it and indent with an extra tab.

> 行长
> Go 没有行长限制。不必担心一行“打穿卡片”。如果你觉得某一行太长，就换行，并额外缩进一个制表符。

Parentheses  
Go needs fewer parentheses than C and Java: control structures (`if`, `for`, `switch`) do not have parentheses in their syntax. Also, the operator precedence hierarchy is shorter and clearer, so

> 括号
> Go 需要的括号比 C 和 Java 少：控制结构（`if`、`for`、`switch`）的语法不需要括号。另外，Go 的运算符优先级层次更少也更清晰，所以：

    x<<8 + y<<16

means what the spacing implies, unlike in the other languages.

> 它的含义就像空格展示的那样，这一点和其他一些语言不同。

## Commentary

> 注释

Go provides C-style `/* */` block comments and C++-style `//` line comments. Line comments are the norm; block comments appear mostly as package comments, but are useful within an expression or to disable large swaths of code.

> Go 提供 C 风格的 `/* */` 块注释，也提供 C++ 风格的 `//` 行注释。行注释是常用形式；块注释多用于包注释，也适合放在表达式内部，或临时屏蔽大段代码。

Comments that appear before top-level declarations, with no intervening newlines, are considered to document the declaration itself. These “doc comments” are the primary documentation for a given Go package or command. For more about doc comments, see “[Go Doc Comments](https://go.dev/doc/comment)”.

> 出现在顶层声明之前、且中间没有空行的注释，会被视为该声明本身的文档。这些“文档注释”是 Go 包或命令的主要文档来源。关于文档注释的更多内容，可参阅 “[Go Doc Comments](https://go.dev/doc/comment)”。

## Names

> 命名

Names are as important in Go as in any other language. They even have semantic effect: the visibility of a name outside a package is determined by whether its first character is upper case. It's therefore worth spending a little time talking about naming conventions in Go programs.

> 命名在 Go 中和在其他语言中一样重要，甚至还带有语义作用：一个名字能否在包外可见，取决于它的首字母是否大写。因此，有必要花一点时间谈谈 Go 程序中的命名约定。

### Package names

> 包名

When a package is imported, the package name becomes an accessor for the contents. After

> 导入一个包后，包名会成为访问其中内容的限定名。例如：

    import "bytes"

the importing package can talk about `bytes.Buffer`. It's helpful if everyone using the package can use the same name to refer to its contents, which implies that the package name should be good: short, concise, evocative. By convention, packages are given lower case, single-word names; there should be no need for underscores or mixedCaps. Err on the side of brevity, since everyone using your package will be typing that name. And don't worry about collisions *a priori*. The package name is only the default name for imports; it need not be unique across all source code, and in the rare case of a collision the importing package can choose a different name to use locally. In any case, confusion is rare because the file name in the import determines just which package is being used.

> 导入方就可以使用 `bytes.Buffer`。如果所有使用这个包的人都能用同一个名字指代其中内容，会很有帮助；这也意味着包名应该取得好：短小、简洁、有表达力。按照约定，包名使用小写的单个单词，不需要下划线或 mixedCaps。宁可偏短，因为所有使用你包的人都会反复输入这个名字。也不必一开始就过分担心重名。包名只是导入时的默认名字，不必在整个代码世界中唯一；少数真正冲突的情况，导入方可以在本地选择别名。无论如何，混淆并不常见，因为 import 路径已经决定了到底使用哪个包。

Another convention is that the package name is the base name of its source directory; the package in `src/encoding/base64` is imported as `"encoding/base64"` but has name `base64`, not `encoding_base64` and not `encodingBase64`.

> 另一个约定是：包名通常是源代码目录的最后一级名称。`src/encoding/base64` 中的包导入路径是 `"encoding/base64"`，但包名是 `base64`，不是 `encoding_base64`，也不是 `encodingBase64`。

The importer of a package will use the name to refer to its contents, so exported names in the package can use that fact to avoid repetition. (Don't use the `import .` notation, which can simplify tests that must run outside the package they are testing, but should otherwise be avoided.) For instance, the buffered reader type in the `bufio` package is called `Reader`, not `BufReader`, because users see it as `bufio.Reader`, which is a clear, concise name. Moreover, because imported entities are always addressed with their package name, `bufio.Reader` does not conflict with `io.Reader`. Similarly, the function to make new instances of `ring.Ring`—which is the definition of a *constructor* in Go—would normally be called `NewRing`, but since `Ring` is the only type exported by the package, and since the package is called `ring`, it's called just `New`, which clients of the package see as `ring.New`. Use the package structure to help you choose good names.

> 导入方会用包名来引用包内内容，因此包中的导出名可以利用这一点来避免重复。（不要使用 `import .`。它可以简化那些必须在被测包外运行的测试，但除此之外应避免使用。）例如，`bufio` 包中的缓冲读取器类型叫 `Reader`，而不是 `BufReader`，因为使用者看到的是 `bufio.Reader`，这个名字清楚又简洁。并且，由于导入的实体总是带着包名访问，`bufio.Reader` 不会和 `io.Reader` 冲突。类似地，用来创建 `ring.Ring` 新实例的函数，也就是 Go 中所谓的构造函数，通常可能会叫 `NewRing`；但因为 `Ring` 是该包唯一导出的类型，而且包名是 `ring`，所以它只叫 `New`，调用方看到的是 `ring.New`。要利用包结构来帮助你选择好名字。

Another short example is `once.Do`; `once.Do(setup)` reads well and would not be improved by writing `once.DoOrWaitUntilDone(setup)`. Long names don't automatically make things more readable. A helpful doc comment can often be more valuable than an extra long name.

> 另一个简短例子是 `once.Do`；`once.Do(setup)` 读起来已经很好，把它写成 `once.DoOrWaitUntilDone(setup)` 并不会更好。名字长并不会自动提升可读性。一个有帮助的文档注释，往往比一个过长的名字更有价值。

### Getters

> Getter

Go doesn't provide automatic support for getters and setters. There's nothing wrong with providing getters and setters yourself, and it's often appropriate to do so, but it's neither idiomatic nor necessary to put `Get` into the getter's name. If you have a field called `owner` (lower case, unexported), the getter method should be called `Owner` (upper case, exported), not `GetOwner`. The use of upper-case names for export provides the hook to discriminate the field from the method. A setter function, if needed, will likely be called `SetOwner`. Both names read well in practice:

> Go 不会自动生成 getter 和 setter。你当然可以自己提供它们，而且很多时候这样做也合适；但在 getter 名字里加 `Get` 既不符合 Go 习惯，也没有必要。如果有一个字段叫 `owner`（小写，未导出），对应的 getter 方法应该叫 `Owner`（大写，导出），而不是 `GetOwner`。导出名使用大写这一规则，正好可以把字段和方法区分开。如果需要 setter，通常可以叫 `SetOwner`。这两个名字在实际代码中都很自然：

    owner := obj.Owner()
    if owner != user {
        obj.SetOwner(user)
    }

### Interface names

> 接口名

By convention, one-method interfaces are named by the method name plus an -er suffix or similar modification to construct an agent noun: `Reader`, `Writer`, `Formatter`, `CloseNotifier` etc.

> 按照约定，只有一个方法的接口通常以方法名加 `-er` 后缀，或类似方式构成表示行为者的名词，比如 `Reader`、`Writer`、`Formatter`、`CloseNotifier` 等。

There are a number of such names and it's productive to honor them and the function names they capture. `Read`, `Write`, `Close`, `Flush`, `String` and so on have canonical signatures and meanings. To avoid confusion, don't give your method one of those names unless it has the same signature and meaning. Conversely, if your type implements a method with the same meaning as a method on a well-known type, give it the same name and signature; call your string-converter method `String` not `ToString`.

> 这类名字有很多，遵守它们以及它们所对应的方法命名很有价值。`Read`、`Write`、`Close`、`Flush`、`String` 等都有公认的签名和含义。为了避免混淆，除非你的方法具有相同的签名和含义，否则不要使用这些名字。反过来，如果你的类型实现了一个与知名类型上的方法含义相同的方法，就使用相同的名字和签名；字符串转换方法应叫 `String`，而不是 `ToString`。

### MixedCaps

> MixedCaps

Finally, the convention in Go is to use `MixedCaps` or `mixedCaps` rather than underscores to write multiword names.

> 最后，Go 的约定是使用 `MixedCaps` 或 `mixedCaps` 来书写多词名字，而不是使用下划线。

## Semicolons

> 分号

Like C, Go's formal grammar uses semicolons to terminate statements, but unlike in C, those semicolons do not appear in the source. Instead the lexer uses a simple rule to insert semicolons automatically as it scans, so the input text is mostly free of them.

> 和 C 一样，Go 的形式语法使用分号结束语句；但不同的是，这些分号通常不会出现在源码中。词法分析器在扫描时会按一条简单规则自动插入分号，因此输入文本里基本不需要写分号。

The rule is this. If the last token before a newline is an identifier (which includes words like `int` and `float64`), a basic literal such as a number or string constant, or one of the tokens

> 规则是这样的：如果换行前的最后一个记号是标识符（包括 `int`、`float64` 这样的词）、数字或字符串常量等基本字面量，或者是下面这些记号之一：

    break continue fallthrough return ++ -- ) }

the lexer always inserts a semicolon after the token. This could be summarized as, “if the newline comes after a token that could end a statement, insert a semicolon”.

> 词法分析器总会在该记号后插入分号。可以概括为：“如果换行出现在一个可能结束语句的记号之后，就插入分号”。

A semicolon can also be omitted immediately before a closing brace, so a statement such as

> 在右花括号之前也可以省略分号，因此下面这样的语句：

        go func() { for { dst <- <-src } }()

needs no semicolons. Idiomatic Go programs have semicolons only in places such as `for` loop clauses, to separate the initializer, condition, and continuation elements. They are also necessary to separate multiple statements on a line, should you write code that way.

> 不需要分号。符合习惯的 Go 程序只会在少数地方出现分号，比如 `for` 循环子句中，用来分隔初始化、条件和后置语句。如果你把多条语句写在同一行，也需要分号来分隔。

One consequence of the semicolon insertion rules is that you cannot put the opening brace of a control structure (`if`, `for`, `switch`, or `select`) on the next line. If you do, a semicolon will be inserted before the brace, which could cause unwanted effects. Write them like this

> 分号插入规则带来的一个结果是：控制结构（`if`、`for`、`switch` 或 `select`）的左花括号不能放到下一行。那样会在花括号前插入分号，可能导致意外结果。应该这样写：

    if i < f() {
        g()
    }

not like this

> 而不是这样：

    if i < f()  // wrong!
    {           // wrong!
        g()
    }

## Control structures

> 控制结构

The control structures of Go are related to those of C but differ in important ways. There is no `do` or `while` loop, only a slightly generalized `for`; `switch` is more flexible; `if` and `switch` accept an optional initialization statement like that of `for`; `break` and `continue` statements take an optional label to identify what to break or continue; and there are new control structures including a type switch and a multiway communications multiplexer, `select`. The syntax is also slightly different: there are no parentheses and the bodies must always be brace-delimited.

> Go 的控制结构与 C 有关联，但有一些重要差异。Go 没有 `do` 或 `while` 循环，只有一个稍微泛化的 `for`；`switch` 更灵活；`if` 和 `switch` 可以像 `for` 一样带一个可选的初始化语句；`break` 和 `continue` 可以带可选标签，用来指明要跳出或继续哪个结构；此外还有类型 switch，以及多路通信复用器 `select`。语法也略有不同：条件不需要括号，语句体必须用花括号包围。

### If

> If

In Go a simple `if` looks like this:

> Go 中一个简单的 `if` 长这样：

    if x > 0 {
        return y
    }

Mandatory braces encourage writing simple `if` statements on multiple lines. It's good style to do so anyway, especially when the body contains a control statement such as a `return` or `break`.

> 强制使用花括号，会鼓励把简单的 `if` 写成多行。无论如何，这都是好风格，尤其是当语句体里包含 `return` 或 `break` 这样的控制语句时。

Since `if` and `switch` accept an initialization statement, it's common to see one used to set up a local variable.

> 因为 `if` 和 `switch` 可以接受初始化语句，所以经常会看到它们用来设置局部变量。

    if err := file.Chmod(0664); err != nil {
        log.Print(err)
        return err
    }

In the Go libraries, you'll find that when an `if` statement doesn't flow into the next statement—that is, the body ends in `break`, `continue`, `goto`, or `return`—the unnecessary `else` is omitted.

> 在 Go 标准库中你会看到：如果一个 `if` 语句不会继续流向后面的语句，也就是语句体以 `break`、`continue`、`goto` 或 `return` 结束，那么不必要的 `else` 会被省略。

    f, err := os.Open(name)
    if err != nil {
        return err
    }
    codeUsing(f)

This is an example of a common situation where code must guard against a sequence of error conditions. The code reads well if the successful flow of control runs down the page, eliminating error cases as they arise. Since error cases tend to end in `return` statements, the resulting code needs no `else` statements.

> 这是一种常见场景：代码需要依次处理一系列错误条件。如果成功路径沿着页面向下展开，遇到错误就立即排除，代码会更好读。由于错误分支通常以 `return` 结束，最终代码就不需要 `else`。

    f, err := os.Open(name)
    if err != nil {
        return err
    }
    d, err := f.Stat()
    if err != nil {
        f.Close()
        return err
    }
    codeUsing(f, d)

### Redeclaration and reassignment

> 重新声明与重新赋值

An aside: The last example in the previous section demonstrates a detail of how the `:=` short declaration form works. The declaration that calls `os.Open` reads,

> 顺带一提：上一节最后的例子展示了 `:=` 短变量声明形式的一个细节。调用 `os.Open` 的声明是：

    f, err := os.Open(name)

This statement declares two variables, `f` and `err`. A few lines later, the call to `f.Stat` reads,

> 这条语句声明了两个变量：`f` 和 `err`。几行之后，调用 `f.Stat` 的语句是：

    d, err := f.Stat()

which looks as if it declares `d` and `err`. Notice, though, that `err` appears in both statements. This duplication is legal: `err` is declared by the first statement, but only *re-assigned* in the second. This means that the call to `f.Stat` uses the existing `err` variable declared above, and just gives it a new value.

> 它看起来像是在声明 `d` 和 `err`。不过注意，`err` 在两条语句里都出现了。这种重复是合法的：`err` 在第一条语句中被声明，在第二条语句中只是被*重新赋值*。也就是说，`f.Stat` 调用使用的是上面已经声明的那个 `err` 变量，只是给它一个新值。

In a `:=` declaration a variable `v` may appear even if it has already been declared, provided:

> 在 `:=` 声明中，一个变量 `v` 即使已经声明过，也可以再次出现在左侧，只要满足下面条件：

- this declaration is in the same scope as the existing declaration of `v` (if `v` is already declared in an outer scope, the declaration will create a new variable §),
- the corresponding value in the initialization is assignable to `v`, and
- there is at least one other variable that is created by the declaration.

> - 这次声明与已有的 `v` 声明处在同一个作用域中；如果 `v` 已经在外层作用域声明过，那么这次声明会创建一个新的变量 §。
> - 初始化中对应的值可以赋给 `v`。
> - 这条声明中至少还有一个其他变量是新创建的。

This unusual property is pure pragmatism, making it easy to use a single `err` value, for example, in a long `if-else` chain. You'll see it used often.

> 这个不太寻常的特性完全是出于实用考虑。它让你可以很方便地在很长的 `if-else` 链中复用同一个 `err` 值。你会经常看到这种写法。

§ It's worth noting here that in Go the scope of function parameters and return values is the same as the function body, even though they appear lexically outside the braces that enclose the body.

> § 这里值得注意的是，在 Go 中，函数参数和返回值的作用域与函数体相同，尽管从词法位置上看，它们出现在包围函数体的花括号之外。

### For

> For

The Go `for` loop is similar to—but not the same as—C's. It unifies `for` and `while` and there is no `do-while`. There are three forms, only one of which has semicolons.

> Go 的 `for` 循环类似 C，但并不相同。它把 `for` 和 `while` 合并到一起，并且没有 `do-while`。`for` 有三种形式，其中只有一种带分号。

    // Like a C for
    for init; condition; post { }

    // Like a C while
    for condition { }

    // Like a C for(;;)
    for { }

Short declarations make it easy to declare the index variable right in the loop.

> 短变量声明让你可以很方便地直接在循环中声明索引变量。

    sum := 0
    for i := 0; i < 10; i++ {
        sum += i
    }

If you're looping over an array, slice, string, or map, or reading from a channel, a `range` clause can manage the loop.

> 如果你要遍历数组、切片、字符串或映射，或者从通道读取数据，`range` 子句可以负责管理循环。

    for key, value := range oldMap {
        newMap[key] = value
    }

If you only need the first item in the range (the key or index), drop the second:

> 如果你只需要 `range` 的第一个值，也就是键或索引，可以去掉第二个值：

    for key := range m {
        if key.expired() {
            delete(m, key)
        }
    }

If you only need the second item in the range (the value), use the *blank identifier*, an underscore, to discard the first:

> 如果你只需要第二个值，也就是元素值，可以使用*空白标识符* `_` 丢弃第一个值：

    sum := 0
    for _, value := range array {
        sum += value
    }

The blank identifier has many uses, as described in [a later section](https://go.dev/doc/effective_go#blank).

> 空白标识符有很多用途，后面的[章节](https://go.dev/doc/effective_go#blank)会继续介绍。

For strings, the `range` does more work for you, breaking out individual Unicode code points by parsing the UTF-8. Erroneous encodings consume one byte and produce the replacement rune U+FFFD. (The name (with associated builtin type) `rune` is Go terminology for a single Unicode code point. See [the language specification](https://go.dev/ref/spec#Rune_literals) for details.) The loop

> 对字符串使用 `range` 时，它会替你做更多工作：解析 UTF-8，并拆出一个个 Unicode 码点。错误的编码会消耗一个字节，并生成替代字符 U+FFFD。（`rune` 这个名字以及对应的内置类型，是 Go 中表示单个 Unicode 码点的术语。详情见[语言规范](https://go.dev/ref/spec#Rune_literals)。）下面的循环：

    for pos, char := range "日本\x80語" { // \x80 is an illegal UTF-8 encoding
        fmt.Printf("character %#U starts at byte position %d\n", char, pos)
    }

prints

> 会打印：

    character U+65E5 '日' starts at byte position 0
    character U+672C '本' starts at byte position 3
    character U+FFFD '�' starts at byte position 6
    character U+8A9E '語' starts at byte position 7

Finally, Go has no comma operator and `++` and `--` are statements not expressions. Thus if you want to run multiple variables in a `for` you should use parallel assignment (although that precludes `++` and `--`).

> 最后，Go 没有逗号运算符，并且 `++`、`--` 是语句，不是表达式。因此，如果你想在一个 `for` 中同时推进多个变量，应该使用并行赋值；不过这样就不能使用 `++` 和 `--` 了。

    // Reverse a
    for i, j := 0, len(a)-1; i < j; i, j = i+1, j-1 {
        a[i], a[j] = a[j], a[i]
    }

### Switch

> Switch

Go's `switch` is more general than C's. The expressions need not be constants or even integers, the cases are evaluated top to bottom until a match is found, and if the `switch` has no expression it switches on `true`. It's therefore possible—and idiomatic—to write an `if`-`else`-`if`-`else` chain as a `switch`.

> Go 的 `switch` 比 C 更通用。表达式不必是常量，甚至不必是整数；各个 `case` 会从上到下求值，直到找到匹配项；如果 `switch` 没有表达式，它就相当于对 `true` 做匹配。因此，把一串 `if`-`else`-`if`-`else` 写成 `switch` 不仅可行，而且很符合 Go 习惯。

    func unhex(c byte) byte {
        switch {
        case '0' <= c && c <= '9':
            return c - '0'
        case 'a' <= c && c <= 'f':
            return c - 'a' + 10
        case 'A' <= c && c <= 'F':
            return c - 'A' + 10
        }
        return 0
    }

There is no automatic fall through, but cases can be presented in comma-separated lists.

> Go 的 `case` 不会自动贯穿到下一项，但可以用逗号分隔，把多个情况放在同一个 `case` 中。

    func shouldEscape(c byte) bool {
        switch c {
        case ' ', '?', '&', '=', '#', '+', '%':
            return true
        }
        return false
    }

Although they are not nearly as common in Go as some other C-like languages, `break` statements can be used to terminate a `switch` early. Sometimes, though, it's necessary to break out of a surrounding loop, not the switch, and in Go that can be accomplished by putting a label on the loop and "breaking" to that label. This example shows both uses.

> 虽然在 Go 中不像在某些类 C 语言中那样常见，`break` 仍然可以用来提前结束一个 `switch`。不过有时你需要跳出的是外围循环，而不是 `switch` 本身。在 Go 中，可以给循环加标签，然后 `break` 到这个标签。下面的例子展示了两种用法。

    Loop:
        for n := 0; n < len(src); n += size {
            switch {
            case src[n] < sizeOne:
                if validateOnly {
                    break
                }
                size = 1
                update(src[n])

            case src[n] < sizeTwo:
                if n+1 >= len(src) {
                    err = errShortInput
                    break Loop
                }
                if validateOnly {
                    break
                }
                size = 2
                update(src[n] + src[n+1]<<shift)
            }
        }

Of course, the `continue` statement also accepts an optional label but it applies only to loops.

> 当然，`continue` 语句也可以带可选标签，但它只适用于循环。

To close this section, here's a comparison routine for byte slices that uses two `switch` statements:

> 作为本节收尾，下面是一个比较字节切片的函数，它使用了两个 `switch` 语句：

    // Compare returns an integer comparing the two byte slices,
    // lexicographically.
    // The result will be 0 if a == b, -1 if a < b, and +1 if a > b
    func Compare(a, b []byte) int {
        for i := 0; i < len(a) && i < len(b); i++ {
            switch {
            case a[i] > b[i]:
                return 1
            case a[i] < b[i]:
                return -1
            }
        }
        switch {
        case len(a) > len(b):
            return 1
        case len(a) < len(b):
            return -1
        }
        return 0
    }

### Type switch

> 类型 switch

A switch can also be used to discover the dynamic type of an interface variable. Such a *type switch* uses the syntax of a type assertion with the keyword `type` inside the parentheses. If the switch declares a variable in the expression, the variable will have the corresponding type in each clause. It's also idiomatic to reuse the name in such cases, in effect declaring a new variable with the same name but a different type in each case.

> `switch` 也可以用来判断接口变量的动态类型。这种*类型 switch* 使用类型断言的语法，只是在括号里写的是关键字 `type`。如果这个 `switch` 在表达式中声明了变量，那么在每个分支里，该变量都会具有对应的类型。在这种情况下复用同一个变量名也很常见；效果上就是在每个分支中声明了一个同名但类型不同的新变量。

    var t interface{}
    t = functionOfSomeType()
    switch t := t.(type) {
    default:
        fmt.Printf("unexpected type %T\n", t)     // %T prints whatever type t has
    case bool:
        fmt.Printf("boolean %t\n", t)             // t has type bool
    case int:
        fmt.Printf("integer %d\n", t)             // t has type int
    case *bool:
        fmt.Printf("pointer to boolean %t\n", *t) // t has type *bool
    case *int:
        fmt.Printf("pointer to integer %d\n", *t) // t has type *int
    }

## Functions

> 函数

### Multiple return values

> 多返回值

One of Go's unusual features is that functions and methods can return multiple values. This form can be used to improve on a couple of clumsy idioms in C programs: in-band error returns such as `-1` for `EOF` and modifying an argument passed by address.

> Go 的一个不寻常特性是，函数和方法可以返回多个值。这个形式可以改进 C 程序中一些笨拙的惯用法，例如用 `-1` 表示 `EOF` 这类带内错误返回，或者通过传入地址来修改参数以模拟返回值。

In C, a write error is signaled by a negative count with the error code secreted away in a volatile location. In Go, `Write` can return a count *and* an error: “Yes, you wrote some bytes but not all of them because you filled the device”. The signature of the `Write` method on files from package `os` is:

> 在 C 中，写入错误通常通过负数计数表示，而错误码藏在某个易变位置。Go 中，`Write` 可以同时返回写入字节数和错误：意思是“确实写入了一些字节，但没有全部写完，因为设备满了”。`os` 包中文件的 `Write` 方法签名是：

    func (file *File) Write(b []byte) (n int, err error)

and as the documentation says, it returns the number of bytes written and a non-nil `error` when `n` `!=` `len(b)`. This is a common style; see the section on error handling for more examples.

> 正如文档所说，它会返回写入的字节数；当 `n` `!=` `len(b)` 时，还会返回非 `nil` 的 `error`。这是 Go 中常见的风格；更多例子可见错误处理章节。

A similar approach obviates the need to pass a pointer to a return value to simulate a reference parameter. Here's a simple-minded function to grab a number from a position in a byte slice, returning the number and the next position.

> 类似的方法也让我们不必传入指向返回值的指针来模拟引用参数。下面是一个简单函数：从字节切片中的某个位置开始读取一个数字，并返回该数字和下一个位置。

    func nextInt(b []byte, i int) (int, int) {
        for ; i < len(b) && !isDigit(b[i]); i++ {
        }
        x := 0
        for ; i < len(b) && isDigit(b[i]); i++ {
            x = x*10 + int(b[i]) - '0'
        }
        return x, i
    }

You could use it to scan the numbers in an input slice `b` like this:

> 可以像这样用它扫描输入切片 `b` 中的数字：

        for i := 0; i < len(b); {
            x, i = nextInt(b, i)
            fmt.Println(x)
        }

### Named result parameters

> 命名结果参数

The return or result "parameters" of a Go function can be given names and used as regular variables, just like the incoming parameters. When named, they are initialized to the zero values for their types when the function begins; if the function executes a `return` statement with no arguments, the current values of the result parameters are used as the returned values.

> Go 函数的返回值，也就是结果“参数”，可以命名，并且可以像传入参数一样作为普通变量使用。命名后，函数开始执行时它们会被初始化为各自类型的零值；如果函数执行不带参数的 `return` 语句，就会使用这些结果参数当前的值作为返回值。

The names are not mandatory but they can make code shorter and clearer: they're documentation. If we name the results of `nextInt` it becomes obvious which returned `int` is which.

> 这些名字不是必须的，但可以让代码更短、更清楚：它们本身就是文档。如果给 `nextInt` 的结果命名，就能一眼看出哪个返回的 `int` 表示什么。

    func nextInt(b []byte, pos int) (value, nextPos int) {

Because named results are initialized and tied to an unadorned return, they can simplify as well as clarify. Here's a version of `io.ReadFull` that uses them well:

> 因为命名结果会被初始化，并且与不带参数的 `return` 关联，它们既能简化代码，也能让含义更清楚。下面是一个很好地使用命名结果的 `io.ReadFull` 版本：

    func ReadFull(r Reader, buf []byte) (n int, err error) {
        for len(buf) > 0 && err == nil {
            var nr int
            nr, err = r.Read(buf)
            n += nr
            buf = buf[nr:]
        }
        return
    }

### Defer

> Defer

Go's `defer` statement schedules a function call (the *deferred* function) to be run immediately before the function executing the `defer` returns. It's an unusual but effective way to deal with situations such as resources that must be released regardless of which path a function takes to return. The canonical examples are unlocking a mutex or closing a file.

> Go 的 `defer` 语句会安排一次函数调用，也就是*延迟函数*，在当前执行 `defer` 的函数返回前立即运行。这种方式有些特别，但非常有效，尤其适合处理无论函数从哪条路径返回都必须释放的资源。典型例子是解锁互斥锁或关闭文件。

    // Contents returns the file's contents as a string.
    func Contents(filename string) (string, error) {
        f, err := os.Open(filename)
        if err != nil {
            return "", err
        }
        defer f.Close()  // f.Close will run when we're finished.

        var result []byte
        buf := make([]byte, 100)
        for {
            n, err := f.Read(buf[0:])
            result = append(result, buf[0:n]...) // append is discussed later.
            if err != nil {
                if err == io.EOF {
                    break
                }
                return "", err  // f will be closed if we return here.
            }
        }
        return string(result), nil // f will be closed if we return here.
    }

Deferring a call to a function such as `Close` has two advantages. First, it guarantees that you will never forget to close the file, a mistake that's easy to make if you later edit the function to add a new return path. Second, it means that the close sits near the open, which is much clearer than placing it at the end of the function.

> 延迟调用 `Close` 这样的函数有两个好处。第一，它保证你不会忘记关闭文件；如果以后修改函数并新增返回路径，这种错误很容易发生。第二，它让关闭操作靠近打开操作，比把关闭放到函数末尾清楚得多。

The arguments to the deferred function (which include the receiver if the function is a method) are evaluated when the *defer* executes, not when the *call* executes. Besides avoiding worries about variables changing values as the function executes, this means that a single deferred call site can defer multiple function executions. Here's a silly example.

> 延迟函数的参数，包括方法调用中的接收者，会在执行 *defer* 时求值，而不是在真正执行该*调用*时求值。除了避免担心变量在函数执行过程中改变之外，这还意味着同一个 `defer` 调用位置可以延迟多次函数执行。下面是一个小例子。

    for i := 0; i < 5; i++ {
        defer fmt.Printf("%d ", i)
    }

Deferred functions are executed in LIFO order, so this code will cause `4 3 2 1 0` to be printed when the function returns. A more plausible example is a simple way to trace function execution through the program. We could write a couple of simple tracing routines like this:

> 延迟函数按后进先出的顺序执行，因此这段代码会在函数返回时打印 `4 3 2 1 0`。更实际一点的例子是用它简单跟踪程序中的函数执行过程。我们可以写两个简单的跟踪函数：

    func trace(s string)   { fmt.Println("entering:", s) }
    func untrace(s string) { fmt.Println("leaving:", s) }

    // Use them like this:
    func a() {
        trace("a")
        defer untrace("a")
        // do something....
    }

We can do better by exploiting the fact that arguments to deferred functions are evaluated when the `defer` executes. The tracing routine can set up the argument to the untracing routine. This example:

> 利用“延迟函数参数在执行 `defer` 时求值”这一点，还可以写得更好。跟踪函数可以为取消跟踪函数准备参数。下面这个例子：

    func trace(s string) string {
        fmt.Println("entering:", s)
        return s
    }

    func un(s string) {
        fmt.Println("leaving:", s)
    }

    func a() {
        defer un(trace("a"))
        fmt.Println("in a")
    }

    func b() {
        defer un(trace("b"))
        fmt.Println("in b")
        a()
    }

    func main() {
        b()
    }

prints

> 会打印：

    entering: b
    in b
    entering: a
    in a
    leaving: a
    leaving: b

For programmers accustomed to block-level resource management from other languages, `defer` may seem peculiar, but its most interesting and powerful applications come precisely from the fact that it's not block-based but function-based. In the section on `panic` and `recover` we'll see another example of its possibilities.

> 对习惯了其他语言中块级资源管理的程序员来说，`defer` 可能显得有点奇怪；但它最有意思、最强大的用法，恰恰来自它不是基于代码块，而是基于函数。在 `panic` 和 `recover` 的章节中，我们还会看到另一个例子。

## Data

> 数据

### Allocation with `new`

> 使用 `new` 分配

Go has two allocation primitives, the built-in functions `new` and `make`. They do different things and apply to different types, which can be confusing, but the rules are simple. Let's talk about `new` first. It's a built-in function that allocates memory, but unlike its namesakes in some other languages it does not *initialize* the memory, it only *zeros* it. That is, `new(T)` allocates zeroed storage for a new variable of type `T` and returns its address, a value of type `*T`. In Go terminology, it returns a pointer to a newly allocated zero value of type `T`.

> Go 有两个分配原语，也就是内置函数 `new` 和 `make`。它们做的事情不同，适用的类型也不同，所以一开始可能会让人困惑，但规则其实很简单。先说 `new`。它是一个分配内存的内置函数，但不同于其他一些语言中同名的东西，它不会*初始化*内存，只会把内存*置零*。也就是说，`new(T)` 会为类型 `T` 的新变量分配一块置零的存储，并返回它的地址，也就是一个 `*T` 类型的值。用 Go 的术语说，它返回一个指向新分配的 `T` 类型零值的指针。

Starting with Go 1.26, `new` also accepts an (value) expression as an argument, which specifies the initial value of the variable. For example, `new(int64(300))` allocates a new variable of type `int64`, initialized to 300, and returns its address.

> 从 Go 1.26 开始，`new` 也接受一个值表达式作为参数，用来指定变量的初始值。例如，`new(int64(300))` 会分配一个 `int64` 类型的新变量，将它初始化为 300，并返回它的地址。

Since the memory returned by `new` is zeroed, it's helpful to arrange when designing your data structures that the zero value of each type can be used without further initialization. This means a user of the data structure can create one with `new` and get right to work. For example, the documentation for `bytes.Buffer` states that "the zero value for `Buffer` is an empty buffer ready to use." Similarly, `sync.Mutex` does not have an explicit constructor or `Init` method. Instead, the zero value for a `sync.Mutex` is defined to be an unlocked mutex.

> 因为 `new` 返回的内存已经置零，所以在设计数据结构时，让每种类型的零值无需进一步初始化就能使用，会很有帮助。这样使用者可以直接用 `new` 创建一个值并开始使用。例如，`bytes.Buffer` 的文档说明：“`Buffer` 的零值是一个可直接使用的空缓冲区。” 类似地，`sync.Mutex` 没有显式构造函数或 `Init` 方法；它的零值被定义为一个未加锁的互斥锁。

The zero-value-is-useful property works transitively. Consider this type declaration.

> “零值可用”这个性质可以传递。看下面的类型声明：

    type SyncedBuffer struct {
        lock    sync.Mutex
        buffer  bytes.Buffer
    }

Values of type `SyncedBuffer` are also ready to use immediately upon allocation or just declaration. In the next snippet, both `p` and `v` will work correctly without further arrangement.

> `SyncedBuffer` 类型的值在分配或声明之后也可以立即使用。下面的代码片段中，`p` 和 `v` 都无需额外设置就能正常工作。

    p := new(SyncedBuffer)  // type *SyncedBuffer
    var v SyncedBuffer      // type  SyncedBuffer

### Constructors and composite literals

> 构造函数与复合字面量

Sometimes the zero value isn't good enough and an initializing constructor is necessary, as in this example derived from package `os`.

> 有时候零值还不够好，需要一个带初始化逻辑的构造函数，比如下面这个来自 `os` 包的例子。

    func NewFile(fd int, name string) *File {
        if fd < 0 {
            return nil
        }
        f := new(File)
        f.fd = fd
        f.name = name
        f.dirinfo = nil
        f.nepipe = 0
        return f
    }

There's a lot of boilerplate in there. We can simplify it using a *composite literal*, which is an expression that creates a new instance each time it is evaluated.

> 这里有不少样板代码。可以用*复合字面量*简化它。复合字面量是一个表达式，每次求值都会创建一个新实例。

    func NewFile(fd int, name string) *File {
        if fd < 0 {
            return nil
        }
        f := File{fd, name, nil, 0}
        return &f
    }

Note that, unlike in C, it's perfectly OK to return the address of a local variable; the storage associated with the variable survives after the function returns. In fact, taking the address of a composite literal allocates a fresh instance each time it is evaluated, so we can combine these last two lines.

> 注意，和 C 不同，返回局部变量的地址在 Go 中完全没问题；与该变量相关的存储会在函数返回后继续存在。实际上，对复合字面量取地址时，每次求值都会分配一个新的实例，所以可以把最后两行合并起来。

        return &File{fd, name, nil, 0}

The fields of a composite literal are laid out in order and must all be present. However, by labeling the elements explicitly as *field*`:`*value* pairs, the initializers can appear in any order, with the missing ones left as their respective zero values. Thus we could say

> 复合字面量中的字段按顺序排列，并且必须全部给出。不过，如果显式地把元素标成 *field*`:`*value* 这种形式，初始化项就可以任意排序，未给出的字段会保留各自的零值。因此可以这样写：

        return &File{fd: fd, name: name}

As a limiting case, if a composite literal contains no fields at all, it creates a zero value for the type. The expressions `new(File)` and `&File{}` are equivalent.

> 作为边界情况，如果复合字面量完全没有字段，它会创建该类型的零值。表达式 `new(File)` 和 `&File{}` 是等价的。

Composite literals can also be created for arrays, slices, and maps, with the field labels being indices or map keys as appropriate. In these examples, the initializations work regardless of the values of `Enone`, `Eio`, and `Einval`, as long as they are distinct.

> 复合字面量也可以用于数组、切片和映射；字段标签相应地可以是索引或映射键。在下面这些例子中，只要 `Enone`、`Eio` 和 `Einval` 的值彼此不同，初始化都会正确工作。

    a := [...]string   {Enone: "no error", Eio: "Eio", Einval: "invalid argument"}
    s := []string      {Enone: "no error", Eio: "Eio", Einval: "invalid argument"}
    m := map[int]string{Enone: "no error", Eio: "Eio", Einval: "invalid argument"}

### Allocation with `make`

> 使用 `make` 分配

Back to allocation. The built-in function `make(T, `*args*`)` serves a purpose different from `new(T)`. It creates slices, maps, and channels only, and it returns an *initialized* (not *zeroed*) value of type `T` (not `*T`). The reason for the distinction is that these three types represent, under the covers, references to data structures that must be initialized before use. A slice, for example, is a three-item descriptor containing a pointer to the data (inside an array), the length, and the capacity, and until those items are initialized, the slice is `nil`. For slices, maps, and channels, `make` initializes the internal data structure and prepares the value for use. For instance,

> 回到分配的话题。内置函数 `make(T, `*args*`)` 的用途不同于 `new(T)`。它只创建切片、映射和通道，并返回一个类型为 `T` 的*已初始化*值，而不是*置零*值，也不是 `*T`。之所以要区分，是因为这三种类型在底层都表示对某种数据结构的引用，而这些数据结构在使用前必须先初始化。以切片为例，它是一个包含三项的描述符：指向数据（位于数组中）的指针、长度和容量。在这些项初始化之前，切片是 `nil`。对于切片、映射和通道，`make` 会初始化内部数据结构，让这个值可以使用。例如：

    make([]int, 10, 100)

allocates an array of 100 ints and then creates a slice structure with length 10 and a capacity of 100 pointing at the first 10 elements of the array. (When making a slice, the capacity can be omitted; see the section on slices for more information.) In contrast, `new([]int)` returns a pointer to a newly allocated, zeroed slice structure, that is, a pointer to a `nil` slice value.

> 它会分配一个包含 100 个 int 的数组，然后创建一个长度为 10、容量为 100 的切片结构，指向该数组的前 10 个元素。（创建切片时可以省略容量；更多信息见切片章节。）相比之下，`new([]int)` 返回的是一个指向新分配、已置零切片结构的指针，也就是指向一个 `nil` 切片值的指针。

These examples illustrate the difference between `new` and `make`.

> 下面的例子展示了 `new` 和 `make` 的区别。

    var p *[]int = new([]int)       // allocates slice structure; *p == nil; rarely useful
    var v  []int = make([]int, 100) // the slice v now refers to a new array of 100 ints

    // Unnecessarily complex:
    var p *[]int = new([]int)
    *p = make([]int, 100, 100)

    // Idiomatic:
    v := make([]int, 100)

Remember that `make` applies only to maps, slices and channels and does not return a pointer. To obtain an explicit pointer allocate with `new` or take the address of a variable explicitly.

> 记住，`make` 只适用于映射、切片和通道，而且不会返回指针。若要得到明确的指针，应使用 `new` 分配，或者显式对变量取地址。

### Arrays

> 数组

Arrays are useful when planning the detailed layout of memory and sometimes can help avoid allocation, but primarily they are a building block for slices, the subject of the next section. To lay the foundation for that topic, here are a few words about arrays.

> 当你需要精细规划内存布局时，数组很有用，有时也能帮助避免分配；但它们主要是切片的构建基础，下一节会讨论切片。为了铺垫这个主题，先简单说几句数组。

There are major differences between the ways arrays work in Go and C. In Go,

> Go 和 C 中数组的工作方式有很大区别。在 Go 中：

- Arrays are values. Assigning one array to another copies all the elements.
- In particular, if you pass an array to a function, it will receive a *copy* of the array, not a pointer to it.
- The size of an array is part of its type. The types `[10]int` and `[20]int` are distinct.

> - 数组是值。把一个数组赋给另一个数组，会复制所有元素。
> - 特别地，如果把数组传给函数，函数收到的是数组的*副本*，而不是指向它的指针。
> - 数组长度是类型的一部分。`[10]int` 和 `[20]int` 是不同类型。

The value property can be useful but also expensive; if you want C-like behavior and efficiency, you can pass a pointer to the array.

> 数组的值语义有时很有用，但也可能代价较高；如果你想要类似 C 的行为和效率，可以传递数组指针。

    func Sum(a *[3]float64) (sum float64) {
        for _, v := range *a {
            sum += v
        }
        return
    }

    array := [...]float64{7.0, 8.5, 9.1}
    x := Sum(&array)  // Note the explicit address-of operator

But even this style isn't idiomatic Go. Use slices instead.

> 但即便这种写法也不是惯用 Go。应该使用切片。

### Slices

> 切片

Slices wrap arrays to give a more general, powerful, and convenient interface to sequences of data. Except for items with explicit dimension such as transformation matrices, most array programming in Go is done with slices rather than simple arrays.

> 切片包装了数组，为数据序列提供了更通用、更强大也更方便的接口。除了一些具有明确维度的对象，比如变换矩阵，Go 中大多数数组相关编程都使用切片，而不是普通数组。

Slices hold references to an underlying array, and if you assign one slice to another, both refer to the same array. If a function takes a slice argument, changes it makes to the elements of the slice will be visible to the caller, analogous to passing a pointer to the underlying array. A `Read` function can therefore accept a slice argument rather than a pointer and a count; the length within the slice sets an upper limit of how much data to read. Here is the signature of the `Read` method of the `File` type in package `os`:

> 切片持有对底层数组的引用。如果把一个切片赋给另一个切片，二者会引用同一个数组。如果函数接收切片参数，它对切片元素所做的修改会被调用方看到，这类似于传递指向底层数组的指针。因此，`Read` 函数可以接收一个切片参数，而不必接收指针和计数；切片的长度本身就限定了最多读取多少数据。下面是 `os` 包中 `File` 类型的 `Read` 方法签名：

    func (f *File) Read(buf []byte) (n int, err error)

The method returns the number of bytes read and an error value, if any. To read into the first 32 bytes of a larger buffer `buf`, *slice* (here used as a verb) the buffer.

> 该方法返回读取的字节数，以及可能出现的错误。若要读入较大缓冲区 `buf` 的前 32 个字节，可以对缓冲区做*切片*操作；这里的 slice 用作动词。

        n, err := f.Read(buf[0:32])

Such slicing is common and efficient. In fact, leaving efficiency aside for the moment, the following snippet would also read the first 32 bytes of the buffer.

> 这种切片操作常见且高效。实际上，如果暂时不考虑效率，下面这段代码也会读取缓冲区的前 32 个字节。

        var n int
        var err error
        for i := 0; i < 32; i++ {
            nbytes, e := f.Read(buf[i:i+1])  // Read one byte.
            n += nbytes
            if nbytes == 0 || e != nil {
                err = e
                break
            }
        }

The length of a slice may be changed as long as it still fits within the limits of the underlying array; just assign it to a slice of itself. The *capacity* of a slice, accessible by the built-in function `cap`, reports the maximum length the slice may assume. Here is a function to append data to a slice. If the data exceeds the capacity, the slice is reallocated. The resulting slice is returned. The function uses the fact that `len` and `cap` are legal when applied to the `nil` slice, and return 0.

> 只要仍然不超出底层数组的范围，切片的长度就可以改变；把它重新赋成自己的一个切片即可。切片的*容量*可以通过内置函数 `cap` 获得，表示该切片最多可以扩展到多长。下面是一个向切片追加数据的函数。如果数据超出容量，就会重新分配切片。函数会返回结果切片。这里利用了一个事实：对 `nil` 切片调用 `len` 和 `cap` 是合法的，并且都会返回 0。

    func Append(slice, data []byte) []byte {
        l := len(slice)
        if l + len(data) > cap(slice) {  // reallocate
            // Allocate double what's needed, for future growth.
            newSlice := make([]byte, (l+len(data))*2)
            // The copy function is predeclared and works for any slice type.
            copy(newSlice, slice)
            slice = newSlice
        }
        slice = slice[0:l+len(data)]
        copy(slice[l:], data)
        return slice
    }

We must return the slice afterwards because, although `Append` can modify the elements of `slice`, the slice itself (the run-time data structure holding the pointer, length, and capacity) is passed by value.

> 之后必须返回切片，因为虽然 `Append` 可以修改 `slice` 中的元素，但切片本身，也就是运行时保存指针、长度和容量的数据结构，是按值传递的。

The idea of appending to a slice is so useful it's captured by the `append` built-in function. To understand that function's design, though, we need a little more information, so we'll return to it later.

> 向切片追加数据这个想法非常有用，因此 Go 把它做成了内置函数 `append`。不过要理解这个函数的设计，还需要先了解更多背景，所以后面会再回到它。

### Two-dimensional slices

> 二维切片

Go's arrays and slices are one-dimensional. To create the equivalent of a 2D array or slice, it is necessary to define an array-of-arrays or slice-of-slices, like this:

> Go 的数组和切片都是一维的。若要创建相当于二维数组或二维切片的结构，需要定义数组的数组，或者切片的切片，例如：

    type Transform [3][3]float64  // A 3x3 array, really an array of arrays.
    type LinesOfText [][]byte     // A slice of byte slices.

Because slices are variable-length, it is possible to have each inner slice be a different length. That can be a common situation, as in our `LinesOfText` example: each line has an independent length.

> 因为切片长度可变，所以每个内部切片可以有不同长度。这种情况很常见，比如 `LinesOfText` 这个例子中，每一行都有独立的长度。

    text := LinesOfText{
        []byte("Now is the time"),
        []byte("for all good gophers"),
        []byte("to bring some fun to the party."),
    }

Sometimes it's necessary to allocate a 2D slice, a situation that can arise when processing scan lines of pixels, for instance. There are two ways to achieve this. One is to allocate each slice independently; the other is to allocate a single array and point the individual slices into it. Which to use depends on your application. If the slices might grow or shrink, they should be allocated independently to avoid overwriting the next line; if not, it can be more efficient to construct the object with a single allocation. For reference, here are sketches of the two methods. First, a line at a time:

> 有时需要分配一个二维切片，例如处理像素扫描行时就可能遇到。实现方式有两种：一种是独立分配每个切片；另一种是分配一个大数组，然后让各个切片指向其中不同部分。选择哪一种取决于你的应用。如果这些切片可能增长或缩短，就应该独立分配，避免覆盖下一行；如果不会变化，用一次分配构造整个对象可能更高效。下面给出两种方法的示意。先看逐行分配：

    // Allocate the top-level slice.
    picture := make([][]uint8, YSize) // One row per unit of y.
    // Loop over the rows, allocating the slice for each row.
    for i := range picture {
        picture[i] = make([]uint8, XSize)
    }

And now as one allocation, sliced into lines:

> 再看一次性分配，然后切成多行：

    // Allocate the top-level slice, the same as before.
    picture := make([][]uint8, YSize) // One row per unit of y.
    // Allocate one large slice to hold all the pixels.
    pixels := make([]uint8, XSize*YSize) // Has type []uint8 even though picture is [][]uint8.
    // Loop over the rows, slicing each row from the front of the remaining pixels slice.
    for i := range picture {
        picture[i], pixels = pixels[:XSize], pixels[XSize:]
    }

### Maps

> 映射

Maps are a convenient and powerful built-in data structure that associate values of one type (the *key*) with values of another type (the *element* or *value*). The key can be of any type for which the equality operator is defined, such as integers, floating point and complex numbers, strings, pointers, interfaces (as long as the dynamic type supports equality), structs and arrays. Slices cannot be used as map keys, because equality is not defined on them. Like slices, maps hold references to an underlying data structure. If you pass a map to a function that changes the contents of the map, the changes will be visible in the caller.

> 映射是 Go 内置的一种方便且强大的数据结构，它把一种类型的值（*键*）关联到另一种类型的值（*元素*或*值*）。键可以是任何定义了相等运算的类型，例如整数、浮点数和复数、字符串、指针、接口（只要其动态类型支持相等比较）、结构体和数组。切片不能作为映射键，因为切片没有定义相等比较。和切片一样，映射持有对底层数据结构的引用。如果把映射传给函数，而函数修改了映射内容，调用方可以看到这些修改。

Maps can be constructed using the usual composite literal syntax with colon-separated key-value pairs, so it's easy to build them during initialization.

> 可以使用普通复合字面量语法构造映射，键值对之间用冒号分隔，因此在初始化时构建映射很容易。

    var timeZone = map[string]int{
        "UTC":  0*60*60,
        "EST": -5*60*60,
        "CST": -6*60*60,
        "MST": -7*60*60,
        "PST": -8*60*60,
    }

Assigning and fetching map values looks syntactically just like doing the same for arrays and slices except that the index doesn't need to be an integer.

> 给映射赋值和从映射取值，在语法上看起来和数组、切片很像，只不过索引不必是整数。

    offset := timeZone["EST"]

An attempt to fetch a map value with a key that is not present in the map will return the zero value for the type of the entries in the map. For instance, if the map contains integers, looking up a non-existent key will return `0`. A set can be implemented as a map with value type `bool`. Set the map entry to `true` to put the value in the set, and then test it by simple indexing.

> 如果用一个不存在的键去取映射中的值，会得到该映射元素类型的零值。例如，如果映射存的是整数，查找不存在的键会返回 `0`。集合可以用值类型为 `bool` 的映射来实现。把某个键对应的映射项设为 `true`，就表示把该值放入集合；之后通过简单索引即可测试它是否存在。

    attended := map[string]bool{
        "Ann": true,
        "Joe": true,
        ...
    }

    if attended[person] { // will be false if person is not in the map
        fmt.Println(person, "was at the meeting")
    }

Sometimes you need to distinguish a missing entry from a zero value. Is there an entry for `"UTC"` or is that 0 because it's not in the map at all? You can discriminate with a form of multiple assignment.

> 有时你需要区分“项不存在”和“值正好是零值”。比如 `"UTC"` 这个键真的存在，还是只是因为它根本不在映射中所以得到 0？可以用一种多重赋值形式来区分。

    var seconds int
    var ok bool
    seconds, ok = timeZone[tz]

For obvious reasons this is called the “comma ok” idiom. In this example, if `tz` is present, `seconds` will be set appropriately and `ok` will be true; if not, `seconds` will be set to zero and `ok` will be false. Here's a function that puts it together with a nice error report:

> 由于形式很直观，这被称为 “comma ok” 惯用法。在这个例子中，如果 `tz` 存在，`seconds` 会被设为对应值，`ok` 为 true；如果不存在，`seconds` 为零，`ok` 为 false。下面的函数把这个用法和一个友好的错误报告结合起来：

    func offset(tz string) int {
        if seconds, ok := timeZone[tz]; ok {
            return seconds
        }
        log.Println("unknown time zone:", tz)
        return 0
    }

To test for presence in the map without worrying about the actual value, you can use the [blank identifier](https://go.dev/doc/effective_go#blank) (`_`) in place of the usual variable for the value.

> 如果只想测试某个键是否存在，而不关心实际值，可以使用[空白标识符](https://go.dev/doc/effective_go#blank)（`_`）来代替通常接收值的变量。

    _, present := timeZone[tz]

To delete a map entry, use the `delete` built-in function, whose arguments are the map and the key to be deleted. It's safe to do this even if the key is already absent from the map.

> 要删除映射项，使用内置函数 `delete`，参数是映射和要删除的键。即使该键本来就不存在，调用 `delete` 也是安全的。

    delete(timeZone, "PDT")  // Now on Standard Time

### Printing

> 打印

Formatted printing in Go uses a style similar to C's `printf` family but is richer and more general. The functions live in the `fmt` package and have capitalized names: `fmt.Printf`, `fmt.Fprintf`, `fmt.Sprintf` and so on. The string functions (`Sprintf` etc.) return a string rather than filling in a provided buffer.

> Go 的格式化打印风格类似 C 的 `printf` 系列，但更丰富、更通用。这些函数位于 `fmt` 包中，并使用大写名称：`fmt.Printf`、`fmt.Fprintf`、`fmt.Sprintf` 等。字符串函数（如 `Sprintf`）返回字符串，而不是填充调用方提供的缓冲区。

You don't need to provide a format string. For each of `Printf`, `Fprintf` and `Sprintf` there is another pair of functions, for instance `Print` and `Println`. These functions do not take a format string but instead generate a default format for each argument. The `Println` versions also insert a blank between arguments and append a newline to the output while the `Print` versions add blanks only if the operand on neither side is a string. In this example each line produces the same output.

> 你不一定要提供格式字符串。对于 `Printf`、`Fprintf` 和 `Sprintf`，都有对应的另一组函数，例如 `Print` 和 `Println`。这些函数不接收格式字符串，而是为每个参数生成默认格式。`Println` 版本还会在参数之间插入空格，并在输出末尾追加换行；`Print` 版本只有在两侧操作数都不是字符串时才会添加空格。在下面的例子中，每一行都会产生相同输出。

    fmt.Printf("Hello %d\n", 23)
    fmt.Fprint(os.Stdout, "Hello ", 23, "\n")
    fmt.Println("Hello", 23)
    fmt.Println(fmt.Sprint("Hello ", 23))

The formatted print functions `fmt.Fprint` and friends take as a first argument any object that implements the `io.Writer` interface; the variables `os.Stdout` and `os.Stderr` are familiar instances.

> `fmt.Fprint` 及其同类格式化打印函数的第一个参数，可以是任何实现了 `io.Writer` 接口的对象；`os.Stdout` 和 `os.Stderr` 就是大家熟悉的例子。

Here things start to diverge from C. First, the numeric formats such as `%d` do not take flags for signedness or size; instead, the printing routines use the type of the argument to decide these properties.

> 从这里开始，Go 与 C 的差异变得明显。首先，像 `%d` 这样的数字格式不需要用标志来指定有符号性或大小；打印函数会根据参数类型决定这些属性。

    var x uint64 = 1<<64 - 1
    fmt.Printf("%d %x; %d %x\n", x, x, int64(x), int64(x))

prints

> 会打印：

    18446744073709551615 ffffffffffffffff; -1 -1

If you just want the default conversion, such as decimal for integers, you can use the catchall format `%v` (for “value”); the result is exactly what `Print` and `Println` would produce. Moreover, that format can print *any* value, even arrays, slices, structs, and maps. Here is a print statement for the time zone map defined in the previous section.

> 如果只想使用默认转换，例如整数默认十进制，可以使用通用格式 `%v`，其中 v 表示 “value”；结果与 `Print` 和 `Println` 产生的结果完全一致。而且这种格式可以打印*任何*值，甚至包括数组、切片、结构体和映射。下面是打印上一节定义的时区映射的语句。

    fmt.Printf("%v\n", timeZone)  // or just fmt.Println(timeZone)

which gives output:

> 输出为：

    map[CST:-21600 EST:-18000 MST:-25200 PST:-28800 UTC:0]

For maps, `Printf` and friends sort the output lexicographically by key.

> 对映射来说，`Printf` 及其同类函数会按键的字典序排序后输出。

When printing a struct, the modified format `%+v` annotates the fields of the structure with their names, and for any value the alternate format `%#v` prints the value in full Go syntax.

> 打印结构体时，修饰格式 `%+v` 会在输出中标注结构体字段名；对于任何值，替代格式 `%#v` 会按完整的 Go 语法打印该值。

    type T struct {
        a int
        b float64
        c string
    }
    t := &T{ 7, -2.35, "abc\tdef" }
    fmt.Printf("%v\n", t)
    fmt.Printf("%+v\n", t)
    fmt.Printf("%#v\n", t)
    fmt.Printf("%#v\n", timeZone)

prints

> 会打印：

    &{7 -2.35 abc   def}
    &{a:7 b:-2.35 c:abc     def}
    &main.T{a:7, b:-2.35, c:"abc\tdef"}
    map[string]int{"CST":-21600, "EST":-18000, "MST":-25200, "PST":-28800, "UTC":0}

(Note the ampersands.) That quoted string format is also available through `%q` when applied to a value of type `string` or `[]byte`. The alternate format `%#q` will use backquotes instead if possible. (The `%q` format also applies to integers and runes, producing a single-quoted rune constant.) Also, `%x` works on strings, byte arrays and byte slices as well as on integers, generating a long hexadecimal string, and with a space in the format (`% x`) it puts spaces between the bytes.

> 注意其中的 & 符号。对 `string` 或 `[]byte` 类型的值使用 `%q`，也可以得到带引号的字符串格式。替代格式 `%#q` 会在可能时改用反引号。（`%q` 也适用于整数和 rune，会生成单引号形式的 rune 常量。）另外，`%x` 不仅能用于整数，也能用于字符串、字节数组和字节切片，会生成较长的十六进制字符串；如果在格式中加一个空格（`% x`），就会在字节之间插入空格。

Another handy format is `%T`, which prints the *type* of a value.

> 另一个方便的格式是 `%T`，它会打印一个值的*类型*。

    fmt.Printf("%T\n", timeZone)

prints

> 会打印：

    map[string]int

If you want to control the default format for a custom type, all that's required is to define a method with the signature `String() string` on the type. For our simple type `T`, that might look like this.

> 如果想控制自定义类型的默认格式，只需要为该类型定义一个签名为 `String() string` 的方法。对于前面的简单类型 `T`，可以这样写：

    func (t *T) String() string {
        return fmt.Sprintf("%d/%g/%q", t.a, t.b, t.c)
    }
    fmt.Printf("%v\n", t)

to print in the format

> 打印出的格式为：

    7/-2.35/"abc\tdef"

(If you need to print *values* of type `T` as well as pointers to `T`, the receiver for `String` must be of value type; this example used a pointer because that's more efficient and idiomatic for struct types. See the section below on [pointers vs. value receivers](https://go.dev/doc/effective_go#pointers_vs_values) for more information.)

> 如果既需要打印 `T` 类型的*值*，也需要打印指向 `T` 的指针，那么 `String` 的接收者必须是值类型。本例使用指针，是因为对结构体类型来说这样更高效，也更符合习惯。更多信息见后面的[指针接收者与值接收者](https://go.dev/doc/effective_go#pointers_vs_values)章节。

Our `String` method is able to call `Sprintf` because the print routines are fully reentrant and can be wrapped this way. There is one important detail to understand about this approach, however: don't construct a `String` method by calling `Sprintf` in a way that will recur into your `String` method indefinitely. This can happen if the `Sprintf` call attempts to print the receiver directly as a string, which in turn will invoke the method again. It's a common and easy mistake to make, as this example shows.

> 我们的 `String` 方法可以调用 `Sprintf`，因为打印函数是完全可重入的，可以这样包装。不过这种做法有一个重要细节要理解：不要用一种会无限递归回 `String` 方法的方式调用 `Sprintf` 来构造 `String` 方法。如果 `Sprintf` 试图直接把接收者当作字符串打印，就会再次调用这个方法，从而发生递归。这是一个常见且容易犯的错误，如下所示。

    type MyString string

    func (m MyString) String() string {
        return fmt.Sprintf("MyString=%s", m) // Error: will recur forever.
    }

It's also easy to fix: convert the argument to the basic string type, which does not have the method.

> 修复也很简单：把参数转换成基本的字符串类型，而基本字符串类型没有这个方法。

    type MyString string
    func (m MyString) String() string {
        return fmt.Sprintf("MyString=%s", string(m)) // OK: note conversion.
    }

In the [initialization section](https://go.dev/doc/effective_go#initialization) we'll see another technique that avoids this recursion.

> 在[初始化章节](https://go.dev/doc/effective_go#initialization)中，我们会看到另一种避免这种递归的技巧。

Another printing technique is to pass a print routine's arguments directly to another such routine. The signature of `Printf` uses the type `...interface{}` for its final argument to specify that an arbitrary number of parameters (of arbitrary type) can appear after the format.

> 另一种打印技巧是，把一个打印函数收到的参数直接传给另一个打印函数。`Printf` 的签名中，最后一个参数使用 `...interface{}` 类型，表示格式参数之后可以出现任意数量、任意类型的参数。

    func Printf(format string, v ...interface{}) (n int, err error) {

Within the function `Printf`, `v` acts like a variable of type `[]interface{}` but if it is passed to another variadic function, it acts like a regular list of arguments. Here is the implementation of the function `log.Println` we used above. It passes its arguments directly to `fmt.Sprintln` for the actual formatting.

> 在 `Printf` 函数内部，`v` 像一个 `[]interface{}` 类型的变量；但如果把它传给另一个可变参数函数，它又可以像普通参数列表一样使用。下面是前面用过的 `log.Println` 的实现。它把自己的参数直接传给 `fmt.Sprintln` 来做真正的格式化。

    // Println prints to the standard logger in the manner of fmt.Println.
    func Println(v ...interface{}) {
        std.Output(2, fmt.Sprintln(v...))  // Output takes parameters (int, string)
    }

We write `...` after `v` in the nested call to `Sprintln` to tell the compiler to treat `v` as a list of arguments; otherwise it would just pass `v` as a single slice argument.

> 在嵌套调用 `Sprintln` 时，我们在 `v` 后面写 `...`，告诉编译器把 `v` 当作参数列表处理；否则它只会把 `v` 作为一个切片参数传入。

There's even more to printing than we've covered here. See the `godoc` documentation for package `fmt` for the details.

> 关于打印，还有很多这里没有涉及的内容。详情请参阅 `fmt` 包的 `godoc` 文档。

By the way, a `...` parameter can be of a specific type, for instance `...int` for a min function that chooses the least of a list of integers:

> 顺便说一句，`...` 参数也可以是某个具体类型。例如，一个从一组整数中选出最小值的函数，可以使用 `...int`：

    func Min(a ...int) int {
        min := int(^uint(0) >> 1)  // largest int
        for _, i := range a {
            if i < min {
                min = i
            }
        }
        return min
    }

### Append

> Append

Now we have the missing piece we needed to explain the design of the `append` built-in function. The signature of `append` is different from our custom `Append` function above. Schematically, it's like this:

> 现在已经有了说明内置函数 `append` 设计所需的最后一块拼图。`append` 的签名不同于前面自定义的 `Append` 函数。示意上，它像这样：

    func append(slice []T, elements ...T) []T

where *T* is a placeholder for any given type. You can't actually write a function in Go where the type `T` is determined by the caller. That's why `append` is built in: it needs support from the compiler.

> 其中 *T* 是某个具体类型的占位符。你实际上无法在 Go 中写出一个由调用方决定 `T` 类型的普通函数。这也是 `append` 必须做成内置函数的原因：它需要编译器支持。

What `append` does is append the elements to the end of the slice and return the result. The result needs to be returned because, as with our hand-written `Append`, the underlying array may change. This simple example

> `append` 做的事情是把元素追加到切片末尾，并返回结果。之所以必须返回结果，是因为和我们手写的 `Append` 一样，底层数组可能会改变。下面这个简单例子：

    x := []int{1,2,3}
    x = append(x, 4, 5, 6)
    fmt.Println(x)

prints `[1 2 3 4 5 6]`. So `append` works a little like `Printf`, collecting an arbitrary number of arguments.

> 会打印 `[1 2 3 4 5 6]`。所以 `append` 有点像 `Printf`，可以收集任意数量的参数。

But what if we wanted to do what our `Append` does and append a slice to a slice? Easy: use `...` at the call site, just as we did in the call to `Output` above. This snippet produces identical output to the one above.

> 但如果我们想像自定义的 `Append` 那样，把一个切片追加到另一个切片后面呢？很简单：在调用处使用 `...`，就像前面对 `Output` 的调用那样。下面的片段会产生和上面相同的输出。

    x := []int{1,2,3}
    y := []int{4,5,6}
    x = append(x, y...)
    fmt.Println(x)

Without that `...`, it wouldn't compile because the types would be wrong; `y` is not of type `int`.

> 如果没有那个 `...`，代码无法编译，因为类型不匹配；`y` 不是 `int` 类型。

## Initialization

> 初始化

Although it doesn't look superficially very different from initialization in C or C++, initialization in Go is more powerful. Complex structures can be built during initialization and the ordering issues among initialized objects, even among different packages, are handled correctly.

> 表面上看，Go 的初始化和 C 或 C++ 差别不大，但实际上更强大。复杂结构可以在初始化期间构建，而且被初始化对象之间的顺序问题，即使跨包，也会被正确处理。

### Constants

> 常量

Constants in Go are just that—constant. They are created at compile time, even when defined as locals in functions, and can only be numbers, characters (runes), strings or booleans. Because of the compile-time restriction, the expressions that define them must be constant expressions, evaluatable by the compiler. For instance, `1<<3` is a constant expression, while `math.Sin(math.Pi/4)` is not because the function call to `math.Sin` needs to happen at run time.

> Go 中的常量确实就是常量。它们在编译期创建，即使定义在函数局部也是如此，并且只能是数字、字符（rune）、字符串或布尔值。由于有编译期限制，定义常量的表达式必须是编译器可求值的常量表达式。例如，`1<<3` 是常量表达式，而 `math.Sin(math.Pi/4)` 不是，因为调用 `math.Sin` 必须在运行时发生。

In Go, enumerated constants are created using the `iota` enumerator. Since `iota` can be part of an expression and expressions can be implicitly repeated, it is easy to build intricate sets of values.

> 在 Go 中，枚举常量使用 `iota` 枚举器创建。因为 `iota` 可以作为表达式的一部分，而表达式又可以隐式重复，所以很容易构造出复杂的值集合。

    type ByteSize float64

    const (
        _           = iota // ignore first value by assigning to blank identifier
        KB ByteSize = 1 << (10 * iota)
        MB
        GB
        TB
        PB
        EB
        ZB
        YB
    )

The ability to attach a method such as `String` to any user-defined type makes it possible for arbitrary values to format themselves automatically for printing. Although you'll see it most often applied to structs, this technique is also useful for scalar types such as floating-point types like `ByteSize`.

> 可以给任何用户自定义类型附加 `String` 这样的方法，这使得任意值都能在打印时自动格式化自己。虽然这种技巧最常见于结构体，但对标量类型也很有用，例如 `ByteSize` 这样的浮点类型。

    func (b ByteSize) String() string {
        switch {
        case b >= YB:
            return fmt.Sprintf("%.2fYB", b/YB)
        case b >= ZB:
            return fmt.Sprintf("%.2fZB", b/ZB)
        case b >= EB:
            return fmt.Sprintf("%.2fEB", b/EB)
        case b >= PB:
            return fmt.Sprintf("%.2fPB", b/PB)
        case b >= TB:
            return fmt.Sprintf("%.2fTB", b/TB)
        case b >= GB:
            return fmt.Sprintf("%.2fGB", b/GB)
        case b >= MB:
            return fmt.Sprintf("%.2fMB", b/MB)
        case b >= KB:
            return fmt.Sprintf("%.2fKB", b/KB)
        }
        return fmt.Sprintf("%.2fB", b)
    }

The expression `YB` prints as `1.00YB`, while `ByteSize(1e13)` prints as `9.09TB`.

> 表达式 `YB` 会打印为 `1.00YB`，而 `ByteSize(1e13)` 会打印为 `9.09TB`。

The use here of `Sprintf` to implement `ByteSize`'s `String` method is safe (avoids recurring indefinitely) not because of a conversion but because it calls `Sprintf` with `%f`, which is not a string format: `Sprintf` will only call the `String` method when it wants a string, and `%f` wants a floating-point value.

> 这里用 `Sprintf` 实现 `ByteSize` 的 `String` 方法是安全的，不会无限递归；原因不是做了类型转换，而是它用 `%f` 调用 `Sprintf`。`%f` 不是字符串格式：只有当 `Sprintf` 需要字符串时才会调用 `String` 方法，而 `%f` 需要的是浮点值。

### Variables

> 变量

Variables can be initialized just like constants but the initializer can be a general expression computed at run time.

> 变量可以像常量一样初始化，但初始化表达式可以是在运行时计算的一般表达式。

    var (
        home   = os.Getenv("HOME")
        user   = os.Getenv("USER")
        gopath = os.Getenv("GOPATH")
    )

### The init function

> init 函数

Finally, each source file can define its own niladic `init` function to set up whatever state is required. (Actually each file can have multiple `init` functions.) And finally means finally: `init` is called after all the variable declarations in the package have evaluated their initializers, and those are evaluated only after all the imported packages have been initialized.

> 最后，每个源文件都可以定义自己的无参数 `init` 函数，用来设置所需状态。（实际上每个文件可以有多个 `init` 函数。）这里的“最后”确实是最后：`init` 会在包中所有变量声明都完成初始化表达式求值之后才调用，而这些初始化又只会在所有导入包初始化完成之后才进行。

Besides initializations that cannot be expressed as declarations, a common use of `init` functions is to verify or repair correctness of the program state before real execution begins.

> 除了处理那些无法用声明表达的初始化之外，`init` 函数的一个常见用途是在真正执行开始前验证或修正程序状态。

    func init() {
        if user == "" {
            log.Fatal("$USER not set")
        }
        if home == "" {
            home = "/home/" + user
        }
        if gopath == "" {
            gopath = home + "/go"
        }
        // gopath may be overridden by --gopath flag on command line.
        flag.StringVar(&gopath, "gopath", gopath, "override default GOPATH")
    }

## Methods

> 方法

### Pointers vs. Values

> 指针和值

As we saw with `ByteSize`, methods can be defined for any named type (except a pointer or an interface); the receiver does not have to be a struct.

> 正如在 `ByteSize` 中看到的，方法可以定义在任何具名类型上，但指针类型和接口类型除外；接收者不一定必须是结构体。

In the discussion of slices above, we wrote an `Append` function. We can define it as a method on slices instead. To do this, we first declare a named type to which we can bind the method, and then make the receiver for the method a value of that type.

> 在前面对切片的讨论中，我们写了一个 `Append` 函数。也可以把它定义成切片上的方法。为此，先声明一个具名类型，让方法可以绑定到它上面，然后把该类型的值作为方法接收者。

    type ByteSlice []byte

    func (slice ByteSlice) Append(data []byte) []byte {
        // Body exactly the same as the Append function defined above.
    }

This still requires the method to return the updated slice. We can eliminate that clumsiness by redefining the method to take a *pointer* to a `ByteSlice` as its receiver, so the method can overwrite the caller's slice.

> 这样仍然要求方法返回更新后的切片。可以把方法重新定义为接收一个指向 `ByteSlice` 的*指针*，从而消除这个笨拙之处；这样方法就能覆盖调用方的切片。

    func (p *ByteSlice) Append(data []byte) {
        slice := *p
        // Body as above, without the return.
        *p = slice
    }

In fact, we can do even better. If we modify our function so it looks like a standard `Write` method, like this,

> 实际上还可以更进一步。如果把函数改成标准 `Write` 方法的样子：

    func (p *ByteSlice) Write(data []byte) (n int, err error) {
        slice := *p
        // Again as above.
        *p = slice
        return len(data), nil
    }

then the type `*ByteSlice` satisfies the standard interface `io.Writer`, which is handy. For instance, we can print into one.

> 那么 `*ByteSlice` 类型就满足标准接口 `io.Writer`，这很有用。例如，可以向它打印内容。

        var b ByteSlice
        fmt.Fprintf(&b, "This hour has %d days\n", 7)

We pass the address of a `ByteSlice` because only `*ByteSlice` satisfies `io.Writer`. The rule about pointers vs. values for receivers is that value methods can be invoked on pointers and values, but pointer methods can only be invoked on pointers.

> 这里传入 `ByteSlice` 的地址，是因为只有 `*ByteSlice` 满足 `io.Writer`。关于接收者是指针还是值，有一条规则：值方法可以在指针和值上调用，但指针方法只能在指针上调用。

This rule arises because pointer methods can modify the receiver; invoking them on a value would cause the method to receive a copy of the value, so any modifications would be discarded. The language therefore disallows this mistake. There is a handy exception, though. When the value is addressable, the language takes care of the common case of invoking a pointer method on a value by inserting the address operator automatically. In our example, the variable `b` is addressable, so we can call its `Write` method with just `b.Write`. The compiler will rewrite that to `(&b).Write` for us.

> 这条规则的原因是，指针方法可以修改接收者；如果在值上调用它们，方法收到的是该值的副本，任何修改都会被丢弃。因此语言禁止这种错误。不过有一个方便的例外：当值是可寻址的，语言会自动插入取地址运算符，处理“在值上调用指针方法”这种常见情况。在我们的例子中，变量 `b` 是可寻址的，所以可以直接调用 `b.Write`；编译器会替我们把它改写成 `(&b).Write`。

By the way, the idea of using `Write` on a slice of bytes is central to the implementation of `bytes.Buffer`.

> 顺便说一句，在字节切片上使用 `Write` 这个思路，是 `bytes.Buffer` 实现的核心。

## Interfaces and other types

> 接口和其他类型

### Interfaces

> 接口

Interfaces in Go provide a way to specify the behavior of an object: if something can do *this*, then it can be used *here*. We've seen a couple of simple examples already; custom printers can be implemented by a `String` method while `Fprintf` can generate output to anything with a `Write` method. Interfaces with only one or two methods are common in Go code, and are usually given a name derived from the method, such as `io.Writer` for something that implements `Write`.

> Go 中的接口提供了一种描述对象行为的方式：如果某个东西能做*这件事*，它就能被用在*这里*。前面已经见过几个简单例子：自定义打印可以通过 `String` 方法实现，而 `Fprintf` 可以向任何带有 `Write` 方法的对象输出内容。只有一两个方法的接口在 Go 代码中很常见，名字通常来自对应的方法，例如实现 `Write` 的对象对应 `io.Writer`。

A type can implement multiple interfaces. For instance, a collection can be sorted by the routines in package `sort` if it implements `sort.Interface`, which contains `Len()`, `Less(i, j int) bool`, and `Swap(i, j int)`, and it could also have a custom formatter. In this contrived example `Sequence` satisfies both.

> 一个类型可以实现多个接口。例如，如果一个集合实现了 `sort.Interface`，也就是包含 `Len()`、`Less(i, j int) bool` 和 `Swap(i, j int)`，它就可以被 `sort` 包中的函数排序；同时它也可以拥有自定义格式化能力。在下面这个刻意构造的例子中，`Sequence` 同时满足这两者。

    type Sequence []int

    // Methods required by sort.Interface.
    func (s Sequence) Len() int {
        return len(s)
    }
    func (s Sequence) Less(i, j int) bool {
        return s[i] < s[j]
    }
    func (s Sequence) Swap(i, j int) {
        s[i], s[j] = s[j], s[i]
    }

    // Copy returns a copy of the Sequence.
    func (s Sequence) Copy() Sequence {
        copy := make(Sequence, 0, len(s))
        return append(copy, s...)
    }

    // Method for printing - sorts the elements before printing.
    func (s Sequence) String() string {
        s = s.Copy() // Make a copy; don't overwrite argument.
        sort.Sort(s)
        str := "["
        for i, elem := range s { // Loop is O(N²); will fix that in next example.
            if i > 0 {
                str += " "
            }
            str += fmt.Sprint(elem)
        }
        return str + "]"
    }

### Conversions

> 转换

The `String` method of `Sequence` is recreating the work that `Sprint` already does for slices. (It also has complexity O(N²), which is poor.) We can share the effort (and also speed it up) if we convert the `Sequence` to a plain `[]int` before calling `Sprint`.

> `Sequence` 的 `String` 方法其实是在重复 `Sprint` 已经为切片做过的工作。（而且它的复杂度是 O(N²)，并不好。）如果在调用 `Sprint` 前先把 `Sequence` 转换成普通的 `[]int`，就可以复用已有工作，同时提升速度。

    func (s Sequence) String() string {
        s = s.Copy()
        sort.Sort(s)
        return fmt.Sprint([]int(s))
    }

This method is another example of the conversion technique for calling `Sprintf` safely from a `String` method. Because the two types (`Sequence` and `[]int`) are the same if we ignore the type name, it's legal to convert between them. The conversion doesn't create a new value, it just temporarily acts as though the existing value has a new type. (There are other legal conversions, such as from integer to floating point, that do create a new value.)

> 这个方法也是一个例子，展示了如何在 `String` 方法中通过类型转换安全地调用 `Sprintf`。如果忽略类型名，`Sequence` 和 `[]int` 这两个类型是相同的，因此可以在它们之间转换。这个转换不会创建新值，只是临时把已有值当作另一种类型来看待。（也有其他合法转换会创建新值，例如从整数转换为浮点数。）

It's an idiom in Go programs to convert the type of an expression to access a different set of methods. As an example, we could use the existing type `sort.IntSlice` to reduce the entire example to this:

> 在 Go 程序中，把表达式转换成另一种类型以访问另一组方法，是一种惯用法。例如，可以使用已有类型 `sort.IntSlice`，把整个例子缩减为：

    type Sequence []int

    // Method for printing - sorts the elements before printing
    func (s Sequence) String() string {
        s = s.Copy()
        sort.IntSlice(s).Sort()
        return fmt.Sprint([]int(s))
    }

Now, instead of having `Sequence` implement multiple interfaces (sorting and printing), we're using the ability of a data item to be converted to multiple types (`Sequence`, `sort.IntSlice` and `[]int`), each of which does some part of the job. That's more unusual in practice but can be effective.

> 现在，我们不是让 `Sequence` 自己实现多个接口（排序和打印），而是利用同一个数据项可以转换成多个类型这一能力：`Sequence`、`sort.IntSlice` 和 `[]int` 分别完成一部分工作。这种写法在实践中不算常见，但有时很有效。

### Interface conversions and type assertions

> 接口转换与类型断言

[Type switches](https://go.dev/doc/effective_go#type_switch) are a form of conversion: they take an interface and, for each case in the switch, in a sense convert it to the type of that case. Here's a simplified version of how the code under `fmt.Printf` turns a value into a string using a type switch. If it's already a string, we want the actual string value held by the interface, while if it has a `String` method we want the result of calling the method.

> [类型 switch](https://go.dev/doc/effective_go#type_switch) 是一种转换形式：它接收一个接口，并且从某种意义上说，会在 `switch` 的每个 `case` 中把它转换成该分支对应的类型。下面是一个简化版本，展示 `fmt.Printf` 底层如何用类型 switch 把一个值转换成字符串。如果它本来就是字符串，我们要的是接口中保存的实际字符串值；如果它有 `String` 方法，我们要的是调用该方法的结果。

    type Stringer interface {
        String() string
    }

    var value interface{} // Value provided by caller.
    switch str := value.(type) {
    case string:
        return str
    case Stringer:
        return str.String()
    }

The first case finds a concrete value; the second converts the interface into another interface. It's perfectly fine to mix types this way.

> 第一个分支找到的是具体值；第二个分支则把接口转换成另一个接口。这样混合类型完全没问题。

What if there's only one type we care about? If we know the value holds a `string` and we just want to extract it? A one-case type switch would do, but so would a *type assertion*. A type assertion takes an interface value and extracts from it a value of the specified explicit type. The syntax borrows from the clause opening a type switch, but with an explicit type rather than the `type` keyword:

> 如果我们只关心一种类型呢？如果知道这个值保存的是 `string`，只想把它取出来，该怎么办？只有一个分支的类型 switch 可以做到，*类型断言*也可以。类型断言接收一个接口值，并从中提取出一个指定显式类型的值。语法借用了类型 switch 开头的形式，但写的是具体类型，而不是 `type` 关键字：

    value.(typeName)

and the result is a new value with the static type `typeName`. That type must either be the concrete type held by the interface, or a second interface type that the value can be converted to. To extract the string we know is in the value, we could write:

> 结果是一个静态类型为 `typeName` 的新值。这个类型必须要么是接口中实际保存的具体类型，要么是该值可以转换成的另一个接口类型。若要取出我们知道存在其中的字符串，可以写：

    str := value.(string)

But if it turns out that the value does not contain a string, the program will crash with a run-time error. To guard against that, use the "comma, ok" idiom to test, safely, whether the value is a string:

> 但如果该值实际上不包含字符串，程序会因运行时错误而崩溃。为了防范这种情况，可以使用 “comma, ok” 惯用法，安全地测试这个值是否为字符串：

    str, ok := value.(string)
    if ok {
        fmt.Printf("string value is: %q\n", str)
    } else {
        fmt.Printf("value is not a string\n")
    }

If the type assertion fails, `str` will still exist and be of type string, but it will have the zero value, an empty string.

> 如果类型断言失败，`str` 仍然存在，类型也仍然是 string，但它会是零值，也就是空字符串。

As an illustration of the capability, here's an `if`-`else` statement that's equivalent to the type switch that opened this section.

> 为了说明这种能力，下面是一个 `if`-`else` 语句，它等价于本节开头的类型 switch。

    if str, ok := value.(string); ok {
        return str
    } else if str, ok := value.(Stringer); ok {
        return str.String()
    }

### Generality

> 通用性

If a type exists only to implement an interface and will never have exported methods beyond that interface, there is no need to export the type itself. Exporting just the interface makes it clear the value has no interesting behavior beyond what is described in the interface. It also avoids the need to repeat the documentation on every instance of a common method.

> 如果一个类型存在的唯一目的就是实现某个接口，并且永远不会有超出该接口的导出方法，那么没有必要导出这个类型本身。只导出接口可以清楚表明：这个值除了接口描述的行为之外，没有其他值得关注的行为。这样也避免了在每个常见方法的实现上重复写文档。

In such cases, the constructor should return an interface value rather than the implementing type. As an example, in the hash libraries both `crc32.NewIEEE` and `adler32.New` return the interface type `hash.Hash32`. Substituting the CRC-32 algorithm for Adler-32 in a Go program requires only changing the constructor call; the rest of the code is unaffected by the change of algorithm.

> 在这种情况下，构造函数应该返回接口值，而不是实现类型。例如，在哈希库中，`crc32.NewIEEE` 和 `adler32.New` 都返回接口类型 `hash.Hash32`。如果在 Go 程序中把 Adler-32 算法替换成 CRC-32，只需要修改构造函数调用；其余代码不会受到算法变化的影响。

A similar approach allows the streaming cipher algorithms in the various `crypto` packages to be separated from the block ciphers they chain together. The `Block` interface in the `crypto/cipher` package specifies the behavior of a block cipher, which provides encryption of a single block of data. Then, by analogy with the `bufio` package, cipher packages that implement this interface can be used to construct streaming ciphers, represented by the `Stream` interface, without knowing the details of the block encryption.

> 类似做法也让各个 `crypto` 包中的流密码算法可以和它们所链接的分组密码分离。`crypto/cipher` 包中的 `Block` 接口规定了分组密码的行为，也就是对单个数据块加密。然后类比 `bufio` 包，实现该接口的密码包可以用来构造由 `Stream` 接口表示的流密码，而不需要知道分组加密的具体细节。

The `crypto/cipher` interfaces look like this:

> `crypto/cipher` 的接口大致如下：

    type Block interface {
        BlockSize() int
        Encrypt(dst, src []byte)
        Decrypt(dst, src []byte)
    }

    type Stream interface {
        XORKeyStream(dst, src []byte)
    }

Here's the definition of the counter mode (CTR) stream, which turns a block cipher into a streaming cipher; notice that the block cipher's details are abstracted away:

> 下面是计数器模式（CTR）流的定义，它把分组密码变成流密码；注意，分组密码的细节已经被抽象掉了：

    // NewCTR returns a Stream that encrypts/decrypts using the given Block in
    // counter mode. The length of iv must be the same as the Block's block size.
    func NewCTR(block Block, iv []byte) Stream

`NewCTR` applies not just to one specific encryption algorithm and data source but to any implementation of the `Block` interface and any `Stream`. Because they return interface values, replacing CTR encryption with other encryption modes is a localized change. The constructor calls must be edited, but because the surrounding code must treat the result only as a `Stream`, it won't notice the difference.

> `NewCTR` 不只适用于某一个具体加密算法和数据源，而是适用于 `Block` 接口的任何实现以及任何 `Stream`。因为这些函数返回的是接口值，所以把 CTR 加密替换成其他加密模式只会影响局部。构造函数调用需要修改，但周围代码只把结果当作 `Stream` 使用，因此不会感知差异。

### Interfaces and methods

> 接口和方法

Since almost anything can have methods attached, almost anything can satisfy an interface. One illustrative example is in the `http` package, which defines the `Handler` interface. Any object that implements `Handler` can serve HTTP requests.

> 由于几乎任何东西都可以附加方法，几乎任何东西也都可以满足接口。一个很有代表性的例子在 `http` 包中，它定义了 `Handler` 接口。任何实现了 `Handler` 的对象都可以处理 HTTP 请求。

    type Handler interface {
        ServeHTTP(ResponseWriter, *Request)
    }

`ResponseWriter` is itself an interface that provides access to the methods needed to return the response to the client. Those methods include the standard `Write` method, so an `http.ResponseWriter` can be used wherever an `io.Writer` can be used. `Request` is a struct containing a parsed representation of the request from the client.

> `ResponseWriter` 本身也是一个接口，提供了向客户端返回响应所需的方法。这些方法包括标准的 `Write` 方法，因此凡是可以使用 `io.Writer` 的地方，也可以使用 `http.ResponseWriter`。`Request` 是一个结构体，包含客户端请求解析后的表示。

For brevity, let's ignore POSTs and assume HTTP requests are always GETs; that simplification does not affect the way the handlers are set up. Here's a trivial implementation of a handler to count the number of times the page is visited.

> 为了简洁，先忽略 POST，假设 HTTP 请求总是 GET；这个简化不会影响处理器的设置方式。下面是一个很简单的处理器实现，用来统计页面被访问的次数。

    // Simple counter server.
    type Counter struct {
        n int
    }

    func (ctr *Counter) ServeHTTP(w http.ResponseWriter, req *http.Request) {
        ctr.n++
        fmt.Fprintf(w, "counter = %d\n", ctr.n)
    }

(Keeping with our theme, note how `Fprintf` can print to an `http.ResponseWriter`.) In a real server, access to `ctr.n` would need protection from concurrent access. See the `sync` and `atomic` packages for suggestions.

> 继续呼应前面的主题，注意 `Fprintf` 可以向 `http.ResponseWriter` 打印。在真实服务器中，对 `ctr.n` 的访问需要防止并发访问问题。可参考 `sync` 和 `atomic` 包中的相关工具。

For reference, here's how to attach such a server to a node on the URL tree.

> 作为参考，下面展示如何把这样的服务器挂到 URL 树上的一个节点。

    import "net/http"
    ...
    ctr := new(Counter)
    http.Handle("/counter", ctr)

But why make `Counter` a struct? An integer is all that's needed. (The receiver needs to be a pointer so the increment is visible to the caller.)

> 但为什么要把 `Counter` 做成结构体？其实一个整数就够了。（接收者需要是指针，这样递增操作才能被调用方看到。）

    // Simpler counter server.
    type Counter int

    func (ctr *Counter) ServeHTTP(w http.ResponseWriter, req *http.Request) {
        *ctr++
        fmt.Fprintf(w, "counter = %d\n", *ctr)
    }

What if your program has some internal state that needs to be notified that a page has been visited? Tie a channel to the web page.

> 如果程序内部有某些状态需要在页面被访问时收到通知，该怎么办？可以把一个通道绑定到网页上。

    // A channel that sends a notification on each visit.
    // (Probably want the channel to be buffered.)
    type Chan chan *http.Request

    func (ch Chan) ServeHTTP(w http.ResponseWriter, req *http.Request) {
        ch <- req
        fmt.Fprint(w, "notification sent")
    }

Finally, let's say we wanted to present on `/args` the arguments used when invoking the server binary. It's easy to write a function to print the arguments.

> 最后，假设我们想在 `/args` 上展示启动服务器二进制文件时使用的参数。写一个打印参数的函数很容易。

    func ArgServer() {
        fmt.Println(os.Args)
    }

How do we turn that into an HTTP server? We could make `ArgServer` a method of some type whose value we ignore, but there's a cleaner way. Since we can define a method for any type except pointers and interfaces, we can write a method for a function. The `http` package contains this code:

> 怎样把它变成 HTTP 服务器呢？我们可以把 `ArgServer` 做成某个类型的方法，然后忽略那个类型的值，但还有更干净的方式。因为除了指针和接口之外，任何类型都可以定义方法，所以也可以给函数定义方法。`http` 包中包含这样的代码：

    // The HandlerFunc type is an adapter to allow the use of
    // ordinary functions as HTTP handlers.  If f is a function
    // with the appropriate signature, HandlerFunc(f) is a
    // Handler object that calls f.
    type HandlerFunc func(ResponseWriter, *Request)

    // ServeHTTP calls f(w, req).
    func (f HandlerFunc) ServeHTTP(w ResponseWriter, req *Request) {
        f(w, req)
    }

`HandlerFunc` is a type with a method, `ServeHTTP`, so values of that type can serve HTTP requests. Look at the implementation of the method: the receiver is a function, `f`, and the method calls `f`. That may seem odd but it's not that different from, say, the receiver being a channel and the method sending on the channel.

> `HandlerFunc` 是一个带有 `ServeHTTP` 方法的类型，因此这种类型的值可以处理 HTTP 请求。看一下这个方法的实现：接收者是一个函数 `f`，方法调用了 `f`。这看起来可能有点奇怪，但和接收者是通道、方法向通道发送数据并没有本质区别。

To make `ArgServer` into an HTTP server, we first modify it to have the right signature.

> 要把 `ArgServer` 变成 HTTP 服务器，先把它改成正确的签名。

    // Argument server.
    func ArgServer(w http.ResponseWriter, req *http.Request) {
        fmt.Fprintln(w, os.Args)
    }

`ArgServer` now has the same signature as `HandlerFunc`, so it can be converted to that type to access its methods, just as we converted `Sequence` to `IntSlice` to access `IntSlice.Sort`. The code to set it up is concise:

> 现在 `ArgServer` 的签名与 `HandlerFunc` 相同，所以可以把它转换成该类型来访问其方法，就像前面把 `Sequence` 转换成 `IntSlice` 来访问 `IntSlice.Sort` 一样。设置代码很简洁：

    http.Handle("/args", http.HandlerFunc(ArgServer))

When someone visits the page `/args`, the handler installed at that page has value `ArgServer` and type `HandlerFunc`. The HTTP server will invoke the method `ServeHTTP` of that type, with `ArgServer` as the receiver, which will in turn call `ArgServer` (via the invocation `f(w, req)` inside `HandlerFunc.ServeHTTP`). The arguments will then be displayed.

> 当有人访问 `/args` 页面时，安装在该页面上的处理器值是 `ArgServer`，类型是 `HandlerFunc`。HTTP 服务器会调用该类型的 `ServeHTTP` 方法，并以 `ArgServer` 作为接收者；随后这个方法会调用 `ArgServer`，也就是 `HandlerFunc.ServeHTTP` 内部的 `f(w, req)`。这样参数就会被显示出来。

In this section we have made an HTTP server from a struct, an integer, a channel, and a function, all because interfaces are just sets of methods, which can be defined for (almost) any type.

> 在这一节中，我们分别用结构体、整数、通道和函数做成了 HTTP 服务器。这一切都成立，是因为接口只是方法集合，而方法几乎可以定义在任何类型上。

## The blank identifier

> 空白标识符

We've mentioned the blank identifier a couple of times now, in the context of [`for` `range` loops](https://go.dev/doc/effective_go#for) and [maps](https://go.dev/doc/effective_go#maps). The blank identifier can be assigned or declared with any value of any type, with the value discarded harmlessly. It's a bit like writing to the Unix `/dev/null` file: it represents a write-only value to be used as a place-holder where a variable is needed but the actual value is irrelevant. It has uses beyond those we've seen already.

> 前面已经在 [`for` `range` 循环](https://go.dev/doc/effective_go#for)和[映射](https://go.dev/doc/effective_go#maps)的上下文中几次提到空白标识符。空白标识符可以用任何类型的任何值赋值或声明，并且该值会被安全地丢弃。它有点像写入 Unix 的 `/dev/null` 文件：它代表一个只写值，用在需要变量但实际值无关紧要的位置。除了前面已经看到的用途，它还有其他用法。

### The blank identifier in multiple assignment

> 多重赋值中的空白标识符

The use of a blank identifier in a `for` `range` loop is a special case of a general situation: multiple assignment.

> 在 `for` `range` 循环中使用空白标识符，是一个更一般场景的特例：多重赋值。

If an assignment requires multiple values on the left side, but one of the values will not be used by the program, a blank identifier on the left-hand-side of the assignment avoids the need to create a dummy variable and makes it clear that the value is to be discarded. For instance, when calling a function that returns a value and an error, but only the error is important, use the blank identifier to discard the irrelevant value.

> 如果一次赋值左侧需要多个值，但其中某个值不会被程序使用，那么在赋值左侧使用空白标识符，就不必创建无意义的临时变量，也能清楚表示该值会被丢弃。例如，调用一个返回值和错误的函数时，如果只有错误重要，就可以用空白标识符丢弃无关的返回值。

    if _, err := os.Stat(path); os.IsNotExist(err) {
        fmt.Printf("%s does not exist\n", path)
    }

Occasionally you'll see code that discards the error value in order to ignore the error; this is terrible practice. Always check error returns; they're provided for a reason.

> 偶尔你会看到有代码为了忽略错误而丢弃错误值；这是很糟糕的做法。一定要检查错误返回值；它们存在是有原因的。

    // Bad! This code will crash if path does not exist.
    fi, _ := os.Stat(path)
    if fi.IsDir() {
        fmt.Printf("%s is a directory\n", path)
    }

### Unused imports and variables

> 未使用的导入和变量

It is an error to import a package or to declare a variable without using it. Unused imports bloat the program and slow compilation, while a variable that is initialized but not used is at least a wasted computation and perhaps indicative of a larger bug. When a program is under active development, however, unused imports and variables often arise and it can be annoying to delete them just to have the compilation proceed, only to have them be needed again later. The blank identifier provides a workaround.

> 导入了包却不使用，或者声明了变量却不使用，在 Go 中都是错误。未使用的导入会让程序膨胀并拖慢编译；初始化了却未使用的变量至少浪费了计算，也可能提示着更大的 bug。不过在程序积极开发过程中，未使用的导入和变量经常会出现。为了让编译继续而删除它们，过一会儿又需要加回来，这很烦。空白标识符提供了一种临时处理办法。

This half-written program has two unused imports (`fmt` and `io`) and an unused variable (`fd`), so it will not compile, but it would be nice to see if the code so far is correct.

> 这个写了一半的程序有两个未使用的导入（`fmt` 和 `io`），还有一个未使用变量（`fd`），因此无法编译；但如果能先看看目前写好的代码是否正确，会很方便。

    package main

    import (
        "fmt"
        "io"
        "log"
        "os"
    )

    func main() {
        fd, err := os.Open("test.go")
        if err != nil {
            log.Fatal(err)
        }
        // TODO: use fd.
    }

To silence complaints about the unused imports, use a blank identifier to refer to a symbol from the imported package. Similarly, assigning the unused variable `fd` to the blank identifier will silence the unused variable error. This version of the program does compile.

> 要消除关于未使用导入的报错，可以用空白标识符引用导入包中的某个符号。类似地，把未使用变量 `fd` 赋给空白标识符，也可以消除未使用变量的错误。下面这个版本可以编译。

    package main

    import (
        "fmt"
        "io"
        "log"
        "os"
    )

    var _ = fmt.Printf // For debugging; delete when done.
    var _ io.Reader    // For debugging; delete when done.

    func main() {
        fd, err := os.Open("test.go")
        if err != nil {
            log.Fatal(err)
        }
        // TODO: use fd.
        _ = fd
    }

By convention, the global declarations to silence import errors should come right after the imports and be commented, both to make them easy to find and as a reminder to clean things up later.

> 按照约定，用来消除导入错误的全局声明应紧跟在导入之后，并加上注释。这样既容易找到，也能提醒你以后清理。

### Import for side effect

> 为副作用而导入

An unused import like `fmt` or `io` in the previous example should eventually be used or removed: blank assignments identify code as a work in progress. But sometimes it is useful to import a package only for its side effects, without any explicit use. For example, during its `init` function, the [`net/http/pprof`](https://go.dev/pkg/net/http/pprof/) package registers HTTP handlers that provide debugging information. It has an exported API, but most clients need only the handler registration and access the data through a web page. To import the package only for its side effects, rename the package to the blank identifier:

> 像前面例子中的 `fmt` 或 `io` 这样的未使用导入，最终应该被使用或删除；空白赋值表明代码还在开发中。但有时只为了副作用导入一个包，而不显式使用它，也很有用。例如，[`net/http/pprof`](https://go.dev/pkg/net/http/pprof/) 包会在自己的 `init` 函数中注册提供调试信息的 HTTP 处理器。它有导出的 API，但大多数使用者只需要处理器注册，然后通过网页访问数据。若只为了副作用导入这个包，可以把包重命名为空白标识符：

    import _ "net/http/pprof"

This form of import makes clear that the package is being imported for its side effects, because there is no other possible use of the package: in this file, it doesn't have a name. (If it did, and we didn't use that name, the compiler would reject the program.)

> 这种导入形式清楚表明：该包是为了副作用而导入的，因为它不可能有其他用途；在这个文件中，它没有名字。（如果有名字却没有使用，编译器会拒绝程序。）

### Interface checks

> 接口检查

As we saw in the discussion of [interfaces](https://go.dev/doc/effective_go#interfaces_and_types) above, a type need not declare explicitly that it implements an interface. Instead, a type implements the interface just by implementing the interface's methods. In practice, most interface conversions are static and therefore checked at compile time. For example, passing an `*os.File` to a function expecting an `io.Reader` will not compile unless `*os.File` implements the `io.Reader` interface.

> 正如前面讨论[接口](https://go.dev/doc/effective_go#interfaces_and_types)时看到的，一个类型不需要显式声明自己实现了某个接口。只要实现了接口的方法，它就实现了这个接口。在实践中，大多数接口转换都是静态的，因此会在编译期检查。例如，如果 `*os.File` 没有实现 `io.Reader` 接口，把它传给一个期望 `io.Reader` 的函数就无法编译。

Some interface checks do happen at run-time, though. One instance is in the [`encoding/json`](https://go.dev/pkg/encoding/json/) package, which defines a [`Marshaler`](https://go.dev/pkg/encoding/json/#Marshaler) interface. When the JSON encoder receives a value that implements that interface, the encoder invokes the value's marshaling method to convert it to JSON instead of doing the standard conversion. The encoder checks this property at run time with a [type assertion](https://go.dev/doc/effective_go#interface_conversions) like:

> 不过也有一些接口检查发生在运行时。一个例子是 [`encoding/json`](https://go.dev/pkg/encoding/json/) 包，它定义了 [`Marshaler`](https://go.dev/pkg/encoding/json/#Marshaler) 接口。当 JSON 编码器收到一个实现了该接口的值时，会调用该值的 marshaling 方法把它转换成 JSON，而不是执行标准转换。编码器会在运行时用[类型断言](https://go.dev/doc/effective_go#interface_conversions)检查这个性质，例如：

    m, ok := val.(json.Marshaler)

If it's necessary only to ask whether a type implements an interface, without actually using the interface itself, perhaps as part of an error check, use the blank identifier to ignore the type-asserted value:

> 如果只是需要询问某个类型是否实现了接口，而不真正使用接口本身，也许只是错误检查的一部分，可以用空白标识符忽略类型断言得到的值：

    if _, ok := val.(json.Marshaler); ok {
        fmt.Printf("value %v of type %T implements json.Marshaler\n", val, val)
    }

One place this situation arises is when it is necessary to guarantee within the package implementing the type that it actually satisfies the interface. If a type—for example, [`json.RawMessage`](https://go.dev/pkg/encoding/json/#RawMessage)—needs a custom JSON representation, it should implement `json.Marshaler`, but there are no static conversions that would cause the compiler to verify this automatically. If the type inadvertently fails to satisfy the interface, the JSON encoder will still work, but will not use the custom implementation. To guarantee that the implementation is correct, a global declaration using the blank identifier can be used in the package:

> 这种情况常见于：在实现某个类型的包内部，需要保证该类型确实满足某个接口。如果一个类型，例如 [`json.RawMessage`](https://go.dev/pkg/encoding/json/#RawMessage)，需要自定义 JSON 表示，它应该实现 `json.Marshaler`；但没有静态转换会让编译器自动验证这一点。如果这个类型不小心没有满足接口，JSON 编码器仍然能工作，只是不会使用自定义实现。为了保证实现正确，可以在包中使用带空白标识符的全局声明：

    var _ json.Marshaler = (*RawMessage)(nil)

In this declaration, the assignment involving a conversion of a `*RawMessage` to a `Marshaler` requires that `*RawMessage` implements `Marshaler`, and that property will be checked at compile time. Should the `json.Marshaler` interface change, this package will no longer compile and we will be on notice that it needs to be updated.

> 在这个声明中，把 `*RawMessage` 转换为 `Marshaler` 的赋值要求 `*RawMessage` 必须实现 `Marshaler`，这个性质会在编译期检查。如果 `json.Marshaler` 接口发生变化，这个包将无法编译，从而提醒我们需要更新实现。

The appearance of the blank identifier in this construct indicates that the declaration exists only for the type checking, not to create a variable. Don't do this for every type that satisfies an interface, though. By convention, such declarations are only used when there are no static conversions already present in the code, which is a rare event.

> 这个结构中出现空白标识符，表示该声明只为类型检查而存在，不是为了创建变量。不过不要给每个满足接口的类型都这么写。按照约定，只有当代码中本来没有静态转换可供检查时才使用这种声明，而这种情况并不常见。

## Embedding

> 嵌入

Go does not provide the typical, type-driven notion of subclassing, but it does have the ability to “borrow” pieces of an implementation by *embedding* types within a struct or interface.

> Go 不提供典型的、由类型驱动的子类化概念，但它可以通过在结构体或接口中*嵌入*类型，来“借用”一部分实现。

Interface embedding is very simple. We've mentioned the `io.Reader` and `io.Writer` interfaces before; here are their definitions.

> 接口嵌入非常简单。前面已经提到过 `io.Reader` 和 `io.Writer` 接口；它们的定义如下。

    type Reader interface {
        Read(p []byte) (n int, err error)
    }

    type Writer interface {
        Write(p []byte) (n int, err error)
    }

The `io` package also exports several other interfaces that specify objects that can implement several such methods. For instance, there is `io.ReadWriter`, an interface containing both `Read` and `Write`. We could specify `io.ReadWriter` by listing the two methods explicitly, but it's easier and more evocative to embed the two interfaces to form the new one, like this:

> `io` 包还导出了其他几个接口，用来描述可以实现多个这类方法的对象。例如，`io.ReadWriter` 接口同时包含 `Read` 和 `Write`。可以通过显式列出两个方法来定义 `io.ReadWriter`，但更简单、更能表达意图的做法是嵌入这两个接口，形成新接口：

    // ReadWriter is the interface that combines the Reader and Writer interfaces.
    type ReadWriter interface {
        Reader
        Writer
    }

This says just what it looks like: A `ReadWriter` can do what a `Reader` does *and* what a `Writer` does; it is a union of the embedded interfaces. Only interfaces can be embedded within interfaces.

> 它的含义和写法一样直观：`ReadWriter` 能做 `Reader` 能做的事，也能做 `Writer` 能做的事；它是被嵌入接口的并集。只有接口可以嵌入到接口中。

The same basic idea applies to structs, but with more far-reaching implications. The `bufio` package has two struct types, `bufio.Reader` and `bufio.Writer`, each of which of course implements the analogous interfaces from package `io`. And `bufio` also implements a buffered reader/writer, which it does by combining a reader and a writer into one struct using embedding: it lists the types within the struct but does not give them field names.

> 同样的基本思想也适用于结构体，但影响更深。`bufio` 包有两个结构体类型：`bufio.Reader` 和 `bufio.Writer`，它们当然分别实现了 `io` 包中对应的接口。`bufio` 还实现了带缓冲的 reader/writer，做法是用嵌入把 reader 和 writer 合并到一个结构体中：在结构体里列出这些类型，但不给它们字段名。

    // ReadWriter stores pointers to a Reader and a Writer.
    // It implements io.ReadWriter.
    type ReadWriter struct {
        *Reader  // *bufio.Reader
        *Writer  // *bufio.Writer
    }

The embedded elements are pointers to structs and of course must be initialized to point to valid structs before they can be used. The `ReadWriter` struct could be written as

> 被嵌入的元素是指向结构体的指针，当然必须先初始化为指向有效结构体，才能使用。`ReadWriter` 结构体也可以写成：

    type ReadWriter struct {
        reader *Reader
        writer *Writer
    }

but then to promote the methods of the fields and to satisfy the `io` interfaces, we would also need to provide forwarding methods, like this:

> 但这样一来，为了提升字段的方法并满足 `io` 接口，我们还需要提供转发方法，例如：

    func (rw *ReadWriter) Read(p []byte) (n int, err error) {
        return rw.reader.Read(p)
    }

By embedding the structs directly, we avoid this bookkeeping. The methods of embedded types come along for free, which means that `bufio.ReadWriter` not only has the methods of `bufio.Reader` and `bufio.Writer`, it also satisfies all three interfaces: `io.Reader`, `io.Writer`, and `io.ReadWriter`.

> 直接嵌入结构体可以避免这些记账式代码。嵌入类型的方法会自动带过来，这意味着 `bufio.ReadWriter` 不仅拥有 `bufio.Reader` 和 `bufio.Writer` 的方法，也同时满足三个接口：`io.Reader`、`io.Writer` 和 `io.ReadWriter`。

There's an important way in which embedding differs from subclassing. When we embed a type, the methods of that type become methods of the outer type, but when they are invoked the receiver of the method is the inner type, not the outer one. In our example, when the `Read` method of a `bufio.ReadWriter` is invoked, it has exactly the same effect as the forwarding method written out above; the receiver is the `reader` field of the `ReadWriter`, not the `ReadWriter` itself.

> 嵌入和子类化有一个重要区别。嵌入某个类型时，该类型的方法会成为外层类型的方法；但调用这些方法时，方法的接收者是内层类型，而不是外层类型。在我们的例子中，调用 `bufio.ReadWriter` 的 `Read` 方法，效果与上面手写的转发方法完全相同；接收者是 `ReadWriter` 的 `reader` 字段，而不是 `ReadWriter` 本身。

Embedding can also be a simple convenience. This example shows an embedded field alongside a regular, named field.

> 嵌入也可以只是为了方便。下面的例子展示了一个嵌入字段和一个普通具名字段并列出现。

    type Job struct {
        Command string
        *log.Logger
    }

The `Job` type now has the `Print`, `Printf`, `Println` and other methods of `*log.Logger`. We could have given the `Logger` a field name, of course, but it's not necessary to do so. And now, once initialized, we can log to the `Job`:

> 现在 `Job` 类型拥有了 `*log.Logger` 的 `Print`、`Printf`、`Println` 等方法。当然，也可以给 `Logger` 一个字段名，但没有必要。初始化之后，就可以直接对 `Job` 记录日志：

    job.Println("starting now...")

The `Logger` is a regular field of the `Job` struct, so we can initialize it in the usual way inside the constructor for `Job`, like this,

> `Logger` 是 `Job` 结构体的常规字段，因此可以在 `Job` 的构造函数中按普通方式初始化它，例如：

    func NewJob(command string, logger *log.Logger) *Job {
        return &Job{command, logger}
    }

or with a composite literal,

> 或者使用复合字面量：

    job := &Job{command, log.New(os.Stderr, "Job: ", log.Ldate)}

If we need to refer to an embedded field directly, the type name of the field, ignoring the package qualifier, serves as a field name, as it did in the `Read` method of our `ReadWriter` struct. Here, if we needed to access the `*log.Logger` of a `Job` variable `job`, we would write `job.Logger`, which would be useful if we wanted to refine the methods of `Logger`.

> 如果需要直接引用嵌入字段，可以使用该字段的类型名作为字段名，忽略包限定名；就像我们在 `ReadWriter` 结构体的 `Read` 方法中那样。这里，如果需要访问 `Job` 变量 `job` 中的 `*log.Logger`，可以写 `job.Logger`；如果想细化 `Logger` 的方法，这会很有用。

    func (job *Job) Printf(format string, args ...interface{}) {
        job.Logger.Printf("%q: %s", job.Command, fmt.Sprintf(format, args...))
    }

Embedding types introduces the problem of name conflicts but the rules to resolve them are simple. First, a field or method `X` hides any other item `X` in a more deeply nested part of the type. If `log.Logger` contained a field or method called `Command`, the `Command` field of `Job` would dominate it.

> 嵌入类型会带来名字冲突问题，但解决规则很简单。首先，字段或方法 `X` 会隐藏类型中更深层嵌套位置的任何其他 `X`。如果 `log.Logger` 中有一个名为 `Command` 的字段或方法，`Job` 的 `Command` 字段会覆盖它。

Second, if the same name appears at the same nesting level, it is usually an error; it would be erroneous to embed `log.Logger` if the `Job` struct contained another field or method called `Logger`. However, if the duplicate name is never mentioned in the program outside the type definition, it is OK. This qualification provides some protection against changes made to types embedded from outside; there is no problem if a field is added that conflicts with another field in another subtype if neither field is ever used.

> 第二，如果同一个名字出现在同一嵌套层级，通常是错误。例如，如果 `Job` 结构体中已经有另一个名为 `Logger` 的字段或方法，再嵌入 `log.Logger` 就是错误。不过，如果这个重复名字从未在类型定义之外的程序中被提到，那就是可以的。这个限定为外部嵌入类型发生变化提供了一些保护：如果新增的字段与另一个子类型中的字段冲突，但两个字段都没有被使用，就不会有问题。

## Concurrency

> 并发

### Share by communicating

> 通过通信共享

Concurrent programming is a large topic and there is space only for some Go-specific highlights here.

> 并发编程是一个很大的主题，这里只介绍一些 Go 特有的重点。

Concurrent programming in many environments is made difficult by the subtleties required to implement correct access to shared variables. Go encourages a different approach in which shared values are passed around on channels and, in fact, never actively shared by separate threads of execution. Only one goroutine has access to the value at any given time. Data races cannot occur, by design. To encourage this way of thinking we have reduced it to a slogan:

> 在很多环境中，并发编程之所以困难，是因为正确访问共享变量需要处理许多微妙细节。Go 鼓励另一种方式：共享值通过通道传递，事实上不会由多个独立执行线程主动共享。在任意时刻，只有一个 goroutine 能访问该值。按这种设计，数据竞争不会发生。为了鼓励这种思考方式，我们把它浓缩成一句口号：

> Do not communicate by sharing memory; instead, share memory by communicating.

> 不要通过共享内存来通信；相反，要通过通信来共享内存。

This approach can be taken too far. Reference counts may be best done by putting a mutex around an integer variable, for instance. But as a high-level approach, using channels to control access makes it easier to write clear, correct programs.

> 这种方式也可能被用过头。例如，引用计数最好可能还是在整数变量外加互斥锁。但从高层思路来看，用通道控制访问，通常更容易写出清晰、正确的程序。

One way to think about this model is to consider a typical single-threaded program running on one CPU. It has no need for synchronization primitives. Now run another such instance; it too needs no synchronization. Now let those two communicate; if the communication is the synchronizer, there's still no need for other synchronization. Unix pipelines, for example, fit this model perfectly. Although Go's approach to concurrency originates in Hoare's Communicating Sequential Processes (CSP), it can also be seen as a type-safe generalization of Unix pipes.

> 可以这样理解这个模型：想象一个运行在单个 CPU 上的典型单线程程序，它不需要同步原语。再运行另一个这样的实例，它也不需要同步。然后让这两个实例通信；如果通信本身就是同步机制，就仍然不需要其他同步。Unix 管道就完美符合这个模型。虽然 Go 的并发方法源自 Hoare 的通信顺序进程（CSP），但也可以看作 Unix 管道的类型安全泛化。

### Goroutines

> Goroutine

They're called *goroutines* because the existing terms—threads, coroutines, processes, and so on—convey inaccurate connotations. A goroutine has a simple model: it is a function executing concurrently with other goroutines in the same address space. It is lightweight, costing little more than the allocation of stack space. And the stacks start small, so they are cheap, and grow by allocating (and freeing) heap storage as required.

> 它们被称为 *goroutine*，是因为已有术语，比如线程、协程、进程等，都会带来不准确的联想。goroutine 的模型很简单：它是在同一地址空间中与其他 goroutine 并发执行的函数。它很轻量，开销只是略高于分配栈空间。栈一开始很小，所以成本很低，并会按需通过分配和释放堆存储来增长。

Goroutines are multiplexed onto multiple OS threads so if one should block, such as while waiting for I/O, others continue to run. Their design hides many of the complexities of thread creation and management.

> goroutine 会被多路复用到多个操作系统线程上，因此如果某个 goroutine 阻塞，例如等待 I/O，其他 goroutine 仍会继续运行。它们的设计隐藏了线程创建和管理中的许多复杂性。

Prefix a function or method call with the `go` keyword to run the call in a new goroutine. When the call completes, the goroutine exits, silently. (The effect is similar to the Unix shell's `&` notation for running a command in the background.)

> 在函数或方法调用前加上 `go` 关键字，就可以在新的 goroutine 中运行这次调用。调用完成后，goroutine 会静默退出。（效果类似 Unix shell 中用 `&` 在后台运行命令。）

    go list.Sort()  // run list.Sort concurrently; don't wait for it.

A function literal can be handy in a goroutine invocation.

> 在 goroutine 调用中，函数字面量很方便。

    func Announce(message string, delay time.Duration) {
        go func() {
            time.Sleep(delay)
            fmt.Println(message)
        }()  // Note the parentheses - must call the function.
    }

In Go, function literals are closures: the implementation makes sure the variables referred to by the function survive as long as they are active.

> 在 Go 中，函数字面量是闭包：实现会确保函数引用到的变量在仍被使用时继续存活。

These examples aren't too practical because the functions have no way of signaling completion. For that, we need channels.

> 这些例子还不太实用，因为函数没有办法通知外部自己已经完成。为此，我们需要通道。

### Channels

> 通道

Like maps, channels are allocated with `make`, and the resulting value acts as a reference to an underlying data structure. If an optional integer parameter is provided, it sets the buffer size for the channel. The default is zero, for an unbuffered or synchronous channel.

> 和映射一样，通道使用 `make` 分配，得到的值表现为对底层数据结构的引用。如果提供一个可选的整数参数，它会设置通道缓冲区大小。默认值为零，表示无缓冲通道，也就是同步通道。

    ci := make(chan int)            // unbuffered channel of integers
    cj := make(chan int, 0)         // unbuffered channel of integers
    cs := make(chan *os.File, 100)  // buffered channel of pointers to Files

Unbuffered channels combine communication—the exchange of a value—with synchronization—guaranteeing that two calculations (goroutines) are in a known state.

> 无缓冲通道把通信和值的交换，与同步结合在一起：它保证两个计算过程，也就是两个 goroutine，处于已知状态。

There are lots of nice idioms using channels. Here's one to get us started. In the previous section we launched a sort in the background. A channel can allow the launching goroutine to wait for the sort to complete.

> 使用通道有很多漂亮的惯用法。先看一个入门例子。上一节中我们在后台启动了排序。通道可以让启动排序的 goroutine 等待排序完成。

    c := make(chan int)  // Allocate a channel.
    // Start the sort in a goroutine; when it completes, signal on the channel.
    go func() {
        list.Sort()
        c <- 1  // Send a signal; value does not matter.
    }()
    doSomethingForAWhile()
    <-c   // Wait for sort to finish; discard sent value.

Receivers always block until there is data to receive. If the channel is unbuffered, the sender blocks until the receiver has received the value. If the channel has a buffer, the sender blocks only until the value has been copied to the buffer; if the buffer is full, this means waiting until some receiver has retrieved a value.

> 接收方总会阻塞，直到有数据可接收。如果通道无缓冲，发送方会阻塞到接收方收到值为止。如果通道有缓冲，发送方只会阻塞到值被复制进缓冲区为止；如果缓冲区已满，就要等到某个接收方取走一个值。

A buffered channel can be used like a semaphore, for instance to limit throughput. In this example, incoming requests are passed to `handle`, which sends a value into the channel, processes the request, and then receives a value from the channel to ready the “semaphore” for the next consumer. The capacity of the channel buffer limits the number of simultaneous calls to `process`.

> 缓冲通道可以像信号量一样使用，例如用于限制吞吐量。在这个例子中，传入请求会被交给 `handle`；它先向通道发送一个值，再处理请求，最后从通道接收一个值，让这个“信号量”为下一个消费者做好准备。通道缓冲区容量限制了同时调用 `process` 的数量。

    var sem = make(chan int, MaxOutstanding)

    func handle(r *Request) {
        sem <- 1    // Wait for active queue to drain.
        process(r)  // May take a long time.
        <-sem       // Done; enable next request to run.
    }

    func Serve(queue chan *Request) {
        for {
            req := <-queue
            go handle(req)  // Don't wait for handle to finish.
        }
    }

Once `MaxOutstanding` handlers are executing `process`, any more will block trying to send into the filled channel buffer, until one of the existing handlers finishes and receives from the buffer.

> 一旦已有 `MaxOutstanding` 个处理器正在执行 `process`，更多处理器在尝试向已满的通道缓冲区发送时就会阻塞，直到某个已有处理器完成并从缓冲区接收一个值。

This design has a problem, though: `Serve` creates a new goroutine for every incoming request, even though only `MaxOutstanding` of them can run at any moment. As a result, the program can consume unlimited resources if the requests come in too fast. We can address that deficiency by changing `Serve` to gate the creation of the goroutines:

> 不过这个设计有个问题：`Serve` 会为每个传入请求创建一个新的 goroutine，尽管任意时刻最多只有 `MaxOutstanding` 个能运行。因此，如果请求来得太快，程序可能消耗无限资源。可以修改 `Serve`，让它控制 goroutine 的创建：

    func Serve(queue chan *Request) {
        for req := range queue {
            sem <- 1
            go func() {
                process(req)
                <-sem
            }()
        }
    }

(Note that in Go versions before 1.22 this code has a bug: the loop variable is shared across all goroutines. See the [Go wiki](https://go.dev/wiki/LoopvarExperiment) for details.)

> 注意，在 Go 1.22 之前的版本中，这段代码有一个 bug：循环变量会被所有 goroutine 共享。详情见 [Go wiki](https://go.dev/wiki/LoopvarExperiment)。

Another approach that manages resources well is to start a fixed number of `handle` goroutines all reading from the request channel. The number of goroutines limits the number of simultaneous calls to `process`. This `Serve` function also accepts a channel on which it will be told to exit; after launching the goroutines it blocks receiving from that channel.

> 另一种能很好管理资源的方法是启动固定数量的 `handle` goroutine，让它们都从请求通道读取。goroutine 的数量会限制同时调用 `process` 的数量。这个 `Serve` 函数还接收一个用于通知退出的通道；启动 goroutine 后，它会阻塞等待从该通道接收退出信号。

    func handle(queue chan *Request) {
        for r := range queue {
            process(r)
        }
    }

    func Serve(clientRequests chan *Request, quit chan bool) {
        // Start handlers
        for i := 0; i < MaxOutstanding; i++ {
            go handle(clientRequests)
        }
        <-quit  // Wait to be told to exit.
    }

### Channels of channels

> 通道的通道

One of the most important properties of Go is that a channel is a first-class value that can be allocated and passed around like any other. A common use of this property is to implement safe, parallel demultiplexing.

> Go 的一个重要性质是，通道是一等值，可以像其他值一样分配和传递。这个性质的一个常见用途，是实现安全的并行解复用。

In the example in the previous section, `handle` was an idealized handler for a request but we didn't define the type it was handling. If that type includes a channel on which to reply, each client can provide its own path for the answer. Here's a schematic definition of type `Request`.

> 在上一节的例子中，`handle` 是一个理想化的请求处理器，但我们没有定义它处理的类型。如果这个类型包含一个用于回复的通道，每个客户端就可以提供自己的接收答案路径。下面是 `Request` 类型的示意定义。

    type Request struct {
        args        []int
        f           func([]int) int
        resultChan  chan int
    }

The client provides a function and its arguments, as well as a channel inside the request object on which to receive the answer.

> 客户端提供一个函数及其参数，并在请求对象中提供一个通道，用来接收答案。

    func sum(a []int) (s int) {
        for _, v := range a {
            s += v
        }
        return
    }

    request := &Request{[]int{3, 4, 5}, sum, make(chan int)}
    // Send request
    clientRequests <- request
    // Wait for response.
    fmt.Printf("answer: %d\n", <-request.resultChan)

On the server side, the handler function is the only thing that changes.

> 在服务器端，只有处理函数需要改变。

    func handle(queue chan *Request) {
        for req := range queue {
            req.resultChan <- req.f(req.args)
        }
    }

There's clearly a lot more to do to make it realistic, but this code is a framework for a rate-limited, parallel, non-blocking RPC system, and there's not a mutex in sight.

> 要把它变成真实可用的系统，显然还需要做很多事；但这段代码已经构成了一个限速、并行、非阻塞 RPC 系统的框架，而且全程看不到互斥锁。

### Parallelization

> 并行化

Another application of these ideas is to parallelize a calculation across multiple CPU cores. If the calculation can be broken into separate pieces that can execute independently, it can be parallelized, with a channel to signal when each piece completes.

> 这些思想的另一个应用，是把计算并行化到多个 CPU 核心上。如果某个计算可以拆成多个能独立执行的部分，就可以并行执行，并用通道通知每一部分何时完成。

Let's say we have an expensive operation to perform on a vector of items, and that the value of the operation on each item is independent, as in this idealized example.

> 假设我们要对一个向量中的各项执行一个昂贵操作，并且每一项的操作结果彼此独立，就像下面这个理想化例子：

    type Vector []float64

    // Apply the operation to v[i], v[i+1] ... up to v[n-1].
    func (v Vector) DoSome(i, n int, u Vector, c chan int) {
        for ; i < n; i++ {
            v[i] += u.Op(v[i])
        }
        c <- 1    // signal that this piece is done
    }

We launch the pieces independently in a loop, one per CPU. They can complete in any order but it doesn't matter; we just count the completion signals by draining the channel after launching all the goroutines.

> 我们在循环中独立启动这些部分，每个 CPU 一个。它们可以以任意顺序完成，这并不重要；启动所有 goroutine 后，只要从通道中取出完成信号并计数即可。

    const numCPU = 4 // number of CPU cores

    func (v Vector) DoAll(u Vector) {
        c := make(chan int, numCPU)  // Buffering optional but sensible.
        for i := 0; i < numCPU; i++ {
            go v.DoSome(i*len(v)/numCPU, (i+1)*len(v)/numCPU, u, c)
        }
        // Drain the channel.
        for i := 0; i < numCPU; i++ {
            <-c    // wait for one task to complete
        }
        // All done.
    }

Rather than create a constant value for numCPU, we can ask the runtime what value is appropriate. The function [`runtime.NumCPU`](https://go.dev/pkg/runtime#NumCPU) returns the number of hardware CPU cores in the machine, so we could write

> 与其为 `numCPU` 创建一个常量值，不如询问运行时系统什么值合适。函数 [`runtime.NumCPU`](https://go.dev/pkg/runtime#NumCPU) 会返回机器上的硬件 CPU 核心数，所以可以写：

    var numCPU = runtime.NumCPU()

There is also a function [`runtime.GOMAXPROCS`](https://go.dev/pkg/runtime#GOMAXPROCS), which reports (or sets) the user-specified number of cores that a Go program can have running simultaneously. It defaults to the value of `runtime.NumCPU` but can be overridden by setting the similarly named shell environment variable or by calling the function with a positive number. Calling it with zero just queries the value. Therefore if we want to honor the user's resource request, we should write

> 还有一个函数 [`runtime.GOMAXPROCS`](https://go.dev/pkg/runtime#GOMAXPROCS)，它会报告或设置 Go 程序可以同时运行的用户指定核心数。默认值是 `runtime.NumCPU`，但可以通过同名 shell 环境变量，或用正数调用该函数来覆盖。用零调用它只是查询当前值。因此，如果想尊重用户的资源设置，应该写：

    var numCPU = runtime.GOMAXPROCS(0)

Be sure not to confuse the ideas of concurrency—structuring a program as independently executing components—and parallelism—executing calculations in parallel for efficiency on multiple CPUs. Although the concurrency features of Go can make some problems easy to structure as parallel computations, Go is a concurrent language, not a parallel one, and not all parallelization problems fit Go's model. For a discussion of the distinction, see the talk cited in [this blog post](https://go.dev/blog/concurrency-is-not-parallelism).

> 一定不要混淆并发和并行。并发是把程序组织成可以独立执行的组件；并行是为了效率，在多个 CPU 上同时执行计算。虽然 Go 的并发特性可以让某些问题很容易组织成并行计算，但 Go 是一门并发语言，不是并行语言，并不是所有并行化问题都适合 Go 的模型。关于二者区别，可参阅[这篇博客](https://go.dev/blog/concurrency-is-not-parallelism)中引用的演讲。

### A leaky buffer

> 漏桶缓冲区

The tools of concurrent programming can even make non-concurrent ideas easier to express. Here's an example abstracted from an RPC package. The client goroutine loops receiving data from some source, perhaps a network. To avoid allocating and freeing buffers, it keeps a free list, and uses a buffered channel to represent it. If the channel is empty, a new buffer gets allocated. Once the message buffer is ready, it's sent to the server on `serverChan`.

> 并发编程工具甚至可以让非并发的思路更容易表达。下面是一个从 RPC 包中抽象出来的例子。客户端 goroutine 循环从某个来源接收数据，可能是网络。为了避免反复分配和释放缓冲区，它维护一个空闲列表，并用缓冲通道表示这个列表。如果通道为空，就分配一个新缓冲区。消息缓冲区准备好后，会通过 `serverChan` 发送给服务器。

    var freeList = make(chan *Buffer, 100)
    var serverChan = make(chan *Buffer)

    func client() {
        for {
            var b *Buffer
            // Grab a buffer if available; allocate if not.
            select {
            case b = <-freeList:
                // Got one; nothing more to do.
            default:
                // None free, so allocate a new one.
                b = new(Buffer)
            }
            load(b)              // Read next message from the net.
            serverChan <- b      // Send to server.
        }
    }

The server loop receives each message from the client, processes it, and returns the buffer to the free list.

> 服务器循环接收来自客户端的每条消息，处理它，然后把缓冲区归还到空闲列表。

    func server() {
        for {
            b := <-serverChan    // Wait for work.
            process(b)
            // Reuse buffer if there's room.
            select {
            case freeList <- b:
                // Buffer on free list; nothing more to do.
            default:
                // Free list full, just carry on.
            }
        }
    }

The client attempts to retrieve a buffer from `freeList`; if none is available, it allocates a fresh one. The server's send to `freeList` puts `b` back on the free list unless the list is full, in which case the buffer is dropped on the floor to be reclaimed by the garbage collector. (The `default` clauses in the `select` statements execute when no other case is ready, meaning that the `selects` never block.) This implementation builds a leaky bucket free list in just a few lines, relying on the buffered channel and the garbage collector for bookkeeping.

> 客户端会尝试从 `freeList` 取一个缓冲区；如果没有可用缓冲区，就新分配一个。服务器向 `freeList` 发送 `b`，会把它放回空闲列表；如果列表已满，缓冲区就被丢弃，之后由垃圾回收器回收。（`select` 语句中的 `default` 分支会在没有其他分支就绪时执行，这意味着这些 `select` 永远不会阻塞。）这个实现只用几行代码就构建了一个漏桶式空闲列表，并依靠缓冲通道和垃圾回收器完成管理。

## Errors

> 错误

Library routines must often return some sort of error indication to the caller. As mentioned earlier, Go's multivalue return makes it easy to return a detailed error description alongside the normal return value. It is good style to use this feature to provide detailed error information. For example, as we'll see, `os.Open` doesn't just return a `nil` pointer on failure, it also returns an error value that describes what went wrong.

> 库函数通常需要向调用方返回某种错误指示。正如前面提到的，Go 的多返回值让函数可以在正常返回值之外，同时返回详细错误说明。利用这个特性提供详细错误信息是一种好风格。例如，后面会看到，`os.Open` 失败时不只是返回一个 `nil` 指针，还会返回一个描述出错原因的错误值。

By convention, errors have type `error`, a simple built-in interface.

> 按照约定，错误的类型是 `error`，这是一个简单的内置接口。

    type error interface {
        Error() string
    }

A library writer is free to implement this interface with a richer model under the covers, making it possible not only to see the error but also to provide some context. As mentioned, alongside the usual `*os.File` return value, `os.Open` also returns an error value. If the file is opened successfully, the error will be `nil`, but when there is a problem, it will hold an `os.PathError`:

> 库作者可以在底层用更丰富的模型实现这个接口，从而不仅能看到错误，还能提供一些上下文。正如前面所说，除了通常的 `*os.File` 返回值，`os.Open` 还会返回一个错误值。如果文件成功打开，错误为 `nil`；如果有问题，它会保存一个 `os.PathError`：

    // PathError records an error and the operation and
    // file path that caused it.
    type PathError struct {
        Op string    // "open", "unlink", etc.
        Path string  // The associated file.
        Err error    // Returned by the system call.
    }

    func (e *PathError) Error() string {
        return e.Op + " " + e.Path + ": " + e.Err.Error()
    }

`PathError`'s `Error` generates a string like this:

> `PathError` 的 `Error` 会生成类似这样的字符串：

    open /etc/passwx: no such file or directory

Such an error, which includes the problematic file name, the operation, and the operating system error it triggered, is useful even if printed far from the call that caused it; it is much more informative than the plain "no such file or directory".

> 这样的错误包含出问题的文件名、操作以及触发的操作系统错误。即使在远离出错调用的位置打印出来，它也很有用；相比单纯的 “no such file or directory”，信息量大得多。

When feasible, error strings should identify their origin, such as by having a prefix naming the operation or package that generated the error. For example, in package `image`, the string representation for a decoding error due to an unknown format is "image: unknown format".

> 在可行时，错误字符串应该标明来源，例如用前缀指出产生错误的操作或包。比如在 `image` 包中，由未知格式导致的解码错误，其字符串表示是 "image: unknown format"。

Callers that care about the precise error details can use a type switch or a type assertion to look for specific errors and extract details. For `PathErrors` this might include examining the internal `Err` field for recoverable failures.

> 关心精确错误细节的调用方，可以使用类型 switch 或类型断言来寻找特定错误并提取详情。对于 `PathError`，这可能包括检查内部的 `Err` 字段，以判断是否是可恢复失败。

    for try := 0; try < 2; try++ {
        file, err = os.Create(filename)
        if err == nil {
            return
        }
        if e, ok := err.(*os.PathError); ok && e.Err == syscall.ENOSPC {
            deleteTempFiles()  // Recover some space.
            continue
        }
        return
    }

The second `if` statement here is another [type assertion](https://go.dev/doc/effective_go#interface_conversions). If it fails, `ok` will be false, and `e` will be `nil`. If it succeeds, `ok` will be true, which means the error was of type `*os.PathError`, and then so is `e`, which we can examine for more information about the error.

> 这里的第二个 `if` 语句是另一个[类型断言](https://go.dev/doc/effective_go#interface_conversions)。如果断言失败，`ok` 为 false，`e` 为 `nil`。如果成功，`ok` 为 true，表示该错误是 `*os.PathError` 类型，`e` 也就是这个类型，因此可以进一步检查它以获取更多错误信息。

### Panic

> Panic

The usual way to report an error to a caller is to return an `error` as an extra return value. The canonical `Read` method is a well-known instance; it returns a byte count and an `error`. But what if the error is unrecoverable? Sometimes the program simply cannot continue.

> 向调用方报告错误的通常方式，是额外返回一个 `error`。典型的 `Read` 方法就是知名例子：它返回字节数和一个 `error`。但如果错误不可恢复怎么办？有时程序确实无法继续运行。

For this purpose, there is a built-in function `panic` that in effect creates a run-time error that will stop the program (but see the next section). The function takes a single argument of arbitrary type—often a string—to be printed as the program dies. It's also a way to indicate that something impossible has happened, such as exiting an infinite loop.

> 为此，Go 提供了内置函数 `panic`，它实际上会创建一个运行时错误，并停止程序（不过请看下一节）。这个函数接收一个任意类型的参数，通常是字符串，会在程序终止时打印出来。它也可以用来表示发生了不可能发生的事情，比如从一个无限循环中退出。

    // A toy implementation of cube root using Newton's method.
    func CubeRoot(x float64) float64 {
        z := x/3   // Arbitrary initial value
        for i := 0; i < 1e6; i++ {
            prevz := z
            z -= (z*z*z-x) / (3*z*z)
            if veryClose(z, prevz) {
                return z
            }
        }
        // A million iterations has not converged; something is wrong.
        panic(fmt.Sprintf("CubeRoot(%g) did not converge", x))
    }

This is only an example but real library functions should avoid `panic`. If the problem can be masked or worked around, it's always better to let things continue to run rather than taking down the whole program. One possible counterexample is during initialization: if the library truly cannot set itself up, it might be reasonable to panic, so to speak.

> 这只是一个例子，真实的库函数应避免使用 `panic`。如果问题可以被屏蔽或绕过，让程序继续运行总是比让整个程序崩溃更好。一个可能的反例是在初始化期间：如果库确实无法完成自身设置，那么 panic 也许是合理的。

    var user = os.Getenv("USER")

    func init() {
        if user == "" {
            panic("no value for $USER")
        }
    }

### Recover

> Recover

When `panic` is called, including implicitly for run-time errors such as indexing a slice out of bounds or failing a type assertion, it immediately stops execution of the current function and begins unwinding the stack of the goroutine, running any deferred functions along the way. If that unwinding reaches the top of the goroutine's stack, the program dies. However, it is possible to use the built-in function `recover` to regain control of the goroutine and resume normal execution.

> 当调用 `panic` 时，包括因切片越界、类型断言失败等运行时错误而隐式发生的 panic，当前函数会立即停止执行，并开始展开该 goroutine 的栈，在展开过程中运行所有延迟函数。如果栈展开到 goroutine 顶部，程序就会终止。不过，可以使用内置函数 `recover` 重新获得该 goroutine 的控制权，并恢复正常执行。

A call to `recover` stops the unwinding and returns the argument passed to `panic`. Because the only code that runs while unwinding is inside deferred functions, `recover` is only useful inside deferred functions.

> 调用 `recover` 会停止栈展开，并返回传给 `panic` 的参数。由于栈展开期间唯一会运行的代码在延迟函数中，`recover` 也只在延迟函数中有用。

One application of `recover` is to shut down a failing goroutine inside a server without killing the other executing goroutines.

> `recover` 的一个用途，是在服务器中关闭失败的 goroutine，而不杀死其他正在执行的 goroutine。

    func server(workChan <-chan *Work) {
        for work := range workChan {
            go safelyDo(work)
        }
    }

    func safelyDo(work *Work) {
        defer func() {
            if err := recover(); err != nil {
                log.Println("work failed:", err)
            }
        }()
        do(work)
    }

In this example, if `do(work)` panics, the result will be logged and the goroutine will exit cleanly without disturbing the others. There's no need to do anything else in the deferred closure; calling `recover` handles the condition completely.

> 在这个例子中，如果 `do(work)` 发生 panic，结果会被记录下来，该 goroutine 会干净退出，不影响其他 goroutine。延迟闭包中不需要再做其他事；调用 `recover` 已经完全处理了这种情况。

Because `recover` always returns `nil` unless called directly from a deferred function, deferred code can call library routines that themselves use `panic` and `recover` without failing. As an example, the deferred function in `safelyDo` might call a logging function before calling `recover`, and that logging code would run unaffected by the panicking state.

> 因为 `recover` 只有在延迟函数中被直接调用时才会返回非 `nil`，所以延迟代码可以调用那些自身使用 `panic` 和 `recover` 的库函数，而不会失效。例如，`safelyDo` 中的延迟函数可以在调用 `recover` 之前先调用日志函数，而日志代码不会受到当前 panic 状态的影响。

With our recovery pattern in place, the `do` function (and anything it calls) can get out of any bad situation cleanly by calling `panic`. We can use that idea to simplify error handling in complex software. Let's look at an idealized version of a `regexp` package, which reports parsing errors by calling `panic` with a local error type. Here's the definition of `Error`, an `error` method, and the `Compile` function.

> 有了这个恢复模式，`do` 函数以及它调用的任何函数，都可以通过调用 `panic` 干净地摆脱糟糕情况。我们可以用这个思路简化复杂软件中的错误处理。看一个理想化的 `regexp` 包版本：它通过用本地错误类型调用 `panic` 来报告解析错误。下面是 `Error` 的定义、一个 `error` 方法，以及 `Compile` 函数。

    // Error is the type of a parse error; it satisfies the error interface.
    type Error string
    func (e Error) Error() string {
        return string(e)
    }

    // error is a method of *Regexp that reports parsing errors by
    // panicking with an Error.
    func (regexp *Regexp) error(err string) {
        panic(Error(err))
    }

    // Compile returns a parsed representation of the regular expression.
    func Compile(str string) (regexp *Regexp, err error) {
        regexp = new(Regexp)
        // doParse will panic if there is a parse error.
        defer func() {
            if e := recover(); e != nil {
                regexp = nil    // Clear return value.
                err = e.(Error) // Will re-panic if not a parse error.
            }
        }()
        return regexp.doParse(str), nil
    }

If `doParse` panics, the recovery block will set the return value to `nil`—deferred functions can modify named return values. It will then check, in the assignment to `err`, that the problem was a parse error by asserting that it has the local type `Error`. If it does not, the type assertion will fail, causing a run-time error that continues the stack unwinding as though nothing had interrupted it. This check means that if something unexpected happens, such as an index out of bounds, the code will fail even though we are using `panic` and `recover` to handle parse errors.

> 如果 `doParse` 发生 panic，恢复代码块会把返回值设为 `nil`，因为延迟函数可以修改命名返回值。然后它会在给 `err` 赋值时，通过断言 panic 值具有本地类型 `Error`，来确认问题确实是解析错误。如果不是，类型断言会失败，导致运行时错误继续展开栈，就好像没有被中断过一样。这个检查意味着，如果发生了意外情况，例如索引越界，即使代码使用 `panic` 和 `recover` 处理解析错误，它仍然会失败。

With error handling in place, the `error` method (because it's a method bound to a type, it's fine, even natural, for it to have the same name as the builtin `error` type) makes it easy to report parse errors without worrying about unwinding the parse stack by hand:

> 有了错误处理之后，`error` 方法会让报告解析错误变得很容易，不必手动展开解析栈。因为它是绑定到某个类型的方法，所以即使和内置的 `error` 类型同名也没问题，甚至很自然：

    if pos == 0 {
        re.error("'*' illegal at start of expression")
    }

Useful though this pattern is, it should be used only within a package. `Parse` turns its internal `panic` calls into `error` values; it does not expose `panics` to its client. That is a good rule to follow.

> 这个模式虽然有用，但应该只在包内部使用。`Parse` 会把内部的 `panic` 调用转换成 `error` 值；它不会把 panic 暴露给客户端。这是一条值得遵守的好规则。

By the way, this re-panic idiom changes the panic value if an actual error occurs. However, both the original and new failures will be presented in the crash report, so the root cause of the problem will still be visible. Thus this simple re-panic approach is usually sufficient—it's a crash after all—but if you want to display only the original value, you can write a little more code to filter unexpected problems and re-panic with the original error. That's left as an exercise for the reader.

> 顺便说一下，如果真的发生错误，这种重新 panic 的惯用法会改变 panic 值。不过，崩溃报告中会同时呈现原始失败和新的失败，因此问题根源仍然可见。所以这种简单的重新 panic 方法通常已经足够，毕竟程序已经崩溃了；但如果你只想显示原始值，可以多写一点代码来过滤意外问题，并用原始错误重新 panic。这留给读者作为练习。

## A web server

> 一个 Web 服务器

Let's finish with a complete Go program, a web server. This one is actually a kind of web re-server. Google provides a service at `chart.apis.google.com` that does automatic formatting of data into charts and graphs. It's hard to use interactively, though, because you need to put the data into the URL as a query. The program here provides a nicer interface to one form of data: given a short piece of text, it calls on the chart server to produce a QR code, a matrix of boxes that encode the text. That image can be grabbed with your cell phone's camera and interpreted as, for instance, a URL, saving you typing the URL into the phone's tiny keyboard.

> 最后用一个完整的 Go 程序收尾：一个 Web 服务器。它其实是一种 Web 转发服务器。Google 在 `chart.apis.google.com` 提供了一个服务，可以自动把数据格式化成图表。不过交互式使用它并不方便，因为你需要把数据作为查询参数放进 URL。这里的程序为一种数据形式提供了更好的界面：给定一小段文本，它调用图表服务器生成一个 QR 码，也就是编码该文本的方块矩阵。可以用手机摄像头读取这张图片，并把它解释成例如 URL，这样就省去了在手机小键盘上输入 URL 的麻烦。

Here's the complete program. An explanation follows.

> 下面是完整程序，之后会进行说明。

    package main

    import (
        "flag"
        "html/template"
        "log"
        "net/http"
    )

    var addr = flag.String("addr", ":1718", "http service address") // Q=17, R=18

    var templ = template.Must(template.New("qr").Parse(templateStr))

    func main() {
        flag.Parse()
        http.Handle("/", http.HandlerFunc(QR))
        err := http.ListenAndServe(*addr, nil)
        if err != nil {
            log.Fatal("ListenAndServe:", err)
        }
    }

    func QR(w http.ResponseWriter, req *http.Request) {
        templ.Execute(w, req.FormValue("s"))
    }

    const templateStr = `
    <html>
    <head>
    <title>QR Link Generator</title>
    </head>
    <body>
    {{if .}}
    <img src="http://chart.apis.google.com/chart?chs=300x300&cht=qr&choe=UTF-8&chl={{.}}" />
    <br>
    {{.}}
    <br>
    <br>
    {{end}}
    <form action="/" name=f method="GET">
        <input maxLength=1024 size=70 name=s value="" title="Text to QR Encode">
        <input type=submit value="Show QR" name=qr>
    </form>
    </body>
    </html>
    `

The pieces up to `main` should be easy to follow. The one flag sets a default HTTP port for our server. The template variable `templ` is where the fun happens. It builds an HTML template that will be executed by the server to display the page; more about that in a moment.

> 到 `main` 之前的部分应该不难理解。唯一的 flag 设置了服务器默认 HTTP 端口。模板变量 `templ` 是有趣的部分。它构建了一个 HTML 模板，服务器会执行这个模板来显示页面；稍后会进一步说明。

The `main` function parses the flags and, using the mechanism we talked about above, binds the function `QR` to the root path for the server. Then `http.ListenAndServe` is called to start the server; it blocks while the server runs.

> `main` 函数解析 flag，并使用前面讨论过的机制，把函数 `QR` 绑定到服务器根路径。然后调用 `http.ListenAndServe` 启动服务器；服务器运行期间该调用会一直阻塞。

`QR` just receives the request, which contains form data, and executes the template on the data in the form value named `s`.

> `QR` 只是接收请求，里面包含表单数据，然后用名为 `s` 的表单值执行模板。

The template package `html/template` is powerful; this program just touches on its capabilities. In essence, it rewrites a piece of HTML text on the fly by substituting elements derived from data items passed to `templ.Execute`, in this case the form value. Within the template text (`templateStr`), double-brace-delimited pieces denote template actions. The piece from `{{if .}}` to `{{end}}` executes only if the value of the current data item, called `.` (dot), is non-empty. That is, when the string is empty, this piece of the template is suppressed.

> `html/template` 模板包很强大；这个程序只展示了它的一点能力。本质上，它会根据传给 `templ.Execute` 的数据项，也就是这里的表单值，动态替换 HTML 文本中的元素。在模板文本（`templateStr`）里，由双花括号包围的部分表示模板动作。从 `{{if .}}` 到 `{{end}}` 的部分，只有当当前数据项，也就是 `.`（点），非空时才会执行。也就是说，当字符串为空时，这部分模板会被抑制。

The two snippets `{{.}}` say to show the data presented to the template—the query string—on the web page. The HTML template package automatically provides appropriate escaping so the text is safe to display.

> 两处 `{{.}}` 表示把传给模板的数据，也就是查询字符串，显示到网页上。HTML 模板包会自动进行适当转义，使文本可以安全显示。

The rest of the template string is just the HTML to show when the page loads. If this is too quick an explanation, see the [documentation](https://go.dev/pkg/html/template/) for the template package for a more thorough discussion.

> 模板字符串剩下的部分，就是页面加载时要显示的 HTML。如果这个解释太简略，可以查看模板包的[文档](https://go.dev/pkg/html/template/)，其中有更完整的讨论。

And there you have it: a useful web server in a few lines of code plus some data-driven HTML text. Go is powerful enough to make a lot happen in a few lines.

> 至此，一个有用的 Web 服务器就完成了：几行代码，加上一些由数据驱动的 HTML 文本。Go 足够强大，可以用很少的代码完成很多事情。
