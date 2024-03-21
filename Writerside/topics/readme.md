# Документация о проекте "AUTOCOMP"
В этой документации будет описание проекта и его некоторые "фичи", бизнес-процессы и алгоритмы работы.

## Суть проекта
Суть проекта заключается в том, что мы создаем магазин, а технически говоря, рекомендательную систему по подбору комплектующих машины для клиентов.


## 1 этап {collapsible="true"}
Для начала мы определяем архитектуру приложения, чтобы понимать как должен взаимодействовать клиент с нашим продуктом.
Был выбран самый удобный вариант взаимодействия на сегодняшний день `21.03.2024` - это Телеграм,
а именно Телеграм Бот на <a href="https://docs.aiogram.dev/en/latest/"><shortcut>aiogram 3.0+</shortcut></a>.

В версии 3 и более были добавлены WebApp-приложения, позволяющие создавать\перенаправлять на страницу в приложении,
откуда можно взаимодействовать с контентом.
Собственно, именно это будет основное, что будет помогать клиенту взаимодействовать с нашим продуктом.

Итак, вот основные сервисы, которые мы будем использовать для проекта:
<procedure title="Сервисы" id="services">
    <step>
        <p>TelegramBot <a href="https://docs.aiogram.dev/en/latest/">
                            <shortcut>Docs</shortcut></a>.</p>
    </step>
    <step>
        <p>FastAPI <a href="https://fastapi.tiangolo.com/"><shortcut>Docs</shortcut></a></p>
    </step>
    <step>
        <p>PostgreSQL - <shortcut>для хранения данных, и управления БП</shortcut></p>
    </step>
    <step>... И т.д. (ДОПИСАТЬ НУЖНО ТОЧНО)</step>
</procedure>

## Add interactive elements

### Tabs
To add switchable content, you can make use of tabs (inject them by starting to type `tab` on a new line):

<tabs>
    <tab title="Markdown">
        <code-block lang="plain text">![Alt Text](new_topic_options.png){ width=450 }</code-block>
    </tab>
    <tab title="Semantic markup">
        <code-block lang="xml">
              <![CDATA[<img src="aaa.png" alt="Alt text" width="450px"/>]]></code-block>
    </tab>
</tabs>

### Convert selection to XML
If you need to extend an element with more functions, you can convert selected content from Markdown to semantic markup.
For example, if you want to merge cells in a table, it's much easier to convert it to XML than do this in Markdown.
Position the caret anywhere in the table and press <shortcut>Alt+Enter</shortcut>:

<!-- <img src="convert_table_to_xml.png" alt="Convert table to XML" width="706" border-effect="line"/> -->

## Feedback and support
Please report any issues, usability improvements, or feature requests to our
<a href="https://youtrack.jetbrains.com/newIssue?project=WRS">YouTrack project</a>
(you will need to register).

You are welcome to join our
<a href="https://jb.gg/WRS_Slack">public Slack workspace</a>.
Before you do, please read our [Code of conduct](https://plugins.jetbrains.com/plugin/20158-writerside/docs/writerside-code-of-conduct.html).
We assume that you’ve read and acknowledged it before joining.

You can also always email us at [writerside@jetbrains.com](mailto:writerside@jetbrains.com).

<seealso>
    <category ref="wrs">
        <a href="https://plugins.jetbrains.com/plugin/20158-writerside/docs/markup-reference.html">Markup reference</a>
        <a href="https://plugins.jetbrains.com/plugin/20158-writerside/docs/manage-table-of-contents.html">Reorder topics in the TOC</a>
        <a href="https://plugins.jetbrains.com/plugin/20158-writerside/docs/local-build.html">Build and publish</a>
        <a href="https://plugins.jetbrains.com/plugin/20158-writerside/docs/configure-search.html">Configure Search</a>
    </category>
</seealso>