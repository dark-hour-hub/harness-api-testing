"""JMeter 5.x 元素 XML 片段模板。

供 generate_jmx.py 使用，每个函数返回一个 JMeter 元素的 XML 字符串。
所有片段只负责拼 XML，不关心业务逻辑（YAML 字段解析在 generate_jmx.py 完成）。
"""

from xml.sax.saxutils import escape as _xml_escape


def escape(value) -> str:
    """转义 XML 文本内容中的 & < >"""
    if value is None:
        return ""
    return _xml_escape(str(value))


def header(value: str = "5.6.3") -> str:
    """jmx 文件头"""
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<jmeterTestPlan version="1.2" properties="5.0" jmeter="{value}">\n'
        '  <hashTree>\n'
    )


def footer() -> str:
    return "  </hashTree>\n</jmeterTestPlan>\n"


def test_plan(name: str = "性能测试计划", comment: str = "") -> str:
    return f'''    <TestPlan guiclass="TestPlanGui" testclass="TestPlan" testname="{escape(name)}" enabled="true">
      <stringProp name="TestPlan.comments">{escape(comment)}</stringProp>
      <boolProp name="TestPlan.functional_mode">false</boolProp>
      <boolProp name="TestPlan.tearDown_on_shutdown">true</boolProp>
      <boolProp name="TestPlan.serialize_threadgroups">false</boolProp>
      <elementProp name="TestPlan.user_defined_variables" elementType="Arguments" guiclass="ArgumentsPanel" testclass="Arguments" testname="用户定义的变量" enabled="true">
        <collectionProp name="Arguments.arguments"/>
      </elementProp>
      <stringProp name="TestPlan.user_define_classpath"></stringProp>
    </TestPlan>
    <hashTree>
'''


def thread_group(name: str, users: int, ramp_up: int, duration: int, loops: int = -1) -> str:
    return f'''      <ThreadGroup guiclass="ThreadGroupGui" testclass="ThreadGroup" testname="{escape(name)}" enabled="true">
        <stringProp name="ThreadGroup.on_sample_error">continue</stringProp>
        <elementProp name="ThreadGroup.main_controller" elementType="LoopController" guiclass="LoopControlPanel" testclass="LoopController" testname="循环控制器" enabled="true">
          <boolProp name="LoopController.continue_forever">false</boolProp>
          <stringProp name="LoopController.loops">{loops}</stringProp>
        </elementProp>
        <stringProp name="ThreadGroup.num_threads">{users}</stringProp>
        <stringProp name="ThreadGroup.ramp_time">{ramp_up}</stringProp>
        <boolProp name="ThreadGroup.scheduler">true</boolProp>
        <stringProp name="ThreadGroup.duration">{duration}</stringProp>
        <stringProp name="ThreadGroup.delay"></stringProp>
        <boolProp name="ThreadGroup.same_user_on_next_iteration">true</boolProp>
      </ThreadGroup>
      <hashTree>
'''


def header_manager(name: str, headers) -> str:
    """headers: list[(name, value)]"""
    items = []
    for hname, hvalue in headers:
        items.append(f'''        <elementProp name="" elementType="Header">
          <stringProp name="Header.name">{escape(hname)}</stringProp>
          <stringProp name="Header.value">{escape(hvalue)}</stringProp>
        </elementProp>''')
    body = "\n".join(items)
    return f'''      <HeaderManager guiclass="HeaderPanel" testclass="HeaderManager" testname="{escape(name)}" enabled="true">
        <collectionProp name="HeaderManager.headers">
{body}
        </collectionProp>
      </HeaderManager>
      <hashTree/>
'''


def once_only_controller(name: str = "登录（每线程一次）") -> str:
    return f'''      <OnceOnlyController guiclass="OnceOnlyControllerGui" testclass="OnceOnlyController" testname="{escape(name)}" enabled="true"/>
      <hashTree>
'''


def http_sampler(name: str, protocol: str, domain: str, port: str, path: str,
                 method: str, body: str = None, query=None) -> str:
    """生成 HTTPSamplerProxy。body 非 None 时用 Raw Post Body（JSON），query 用于 GET。

    Args:
        body: JSON 字符串（POST/PUT/PATCH）
        query: dict，查询参数（GET）
    """
    if body is not None:
        post_body_raw = "        <boolProp name=\"HTTPSampler.postBodyRaw\">true</boolProp>\n"
        args = (f'          <elementProp name="" elementType="HTTPArgument">\n'
                f'            <boolProp name="HTTPArgument.always_encode">false</boolProp>\n'
                f'            <stringProp name="Argument.value">{escape(body)}</stringProp>\n'
                f'            <stringProp name="Argument.metadata">=</stringProp>\n'
                f'          </elementProp>')
    else:
        post_body_raw = ""
        args_list = []
        for qk, qv in (query or {}).items():
            args_list.append(
                f'          <elementProp name="" elementType="HTTPArgument">\n'
                f'            <boolProp name="HTTPArgument.always_encode">true</boolProp>\n'
                f'            <stringProp name="Argument.name">{escape(qk)}</stringProp>\n'
                f'            <stringProp name="Argument.value">{escape(qv)}</stringProp>\n'
                f'            <stringProp name="Argument.metadata">=</stringProp>\n'
                f'          </elementProp>'
            )
        args = "\n".join(args_list)

    return f'''      <HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy" testname="{escape(name)}" enabled="true">
        <elementProp name="HTTPsampler.Arguments" elementType="Arguments" guiclass="HTTPArgumentsPanel" testclass="Arguments" testname="参数" enabled="true">
          <collectionProp name="Arguments.arguments">
{args}
          </collectionProp>
        </elementProp>
{post_body_raw}        <stringProp name="HTTPSampler.domain">{escape(domain)}</stringProp>
        <stringProp name="HTTPSampler.port">{escape(port)}</stringProp>
        <stringProp name="HTTPSampler.protocol">{escape(protocol)}</stringProp>
        <stringProp name="HTTPSampler.contentEncoding">UTF-8</stringProp>
        <stringProp name="HTTPSampler.path">{escape(path)}</stringProp>
        <stringProp name="HTTPSampler.method">{escape(method)}</stringProp>
        <boolProp name="HTTPSampler.follow_redirects">true</boolProp>
        <boolProp name="HTTPSampler.auto_redirects">false</boolProp>
        <boolProp name="HTTPSampler.use_keepalive">true</boolProp>
        <boolProp name="HTTPSampler.DO_MULTIPART_POST">false</boolProp>
        <stringProp name="HTTPSampler.embedded_url_re"></stringProp>
        <stringProp name="HTTPSampler.connect_timeout"></stringProp>
        <stringProp name="HTTPSampler.response_timeout"></stringProp>
      </HTTPSamplerProxy>
      <hashTree>
'''


def json_extractor(name: str, varname: str, jsonpath: str, default: str = "NOT_FOUND") -> str:
    return f'''        <JSONPostProcessor guiclass="JSONPostProcessorGui" testclass="JSONPostProcessor" testname="{escape(name)}" enabled="true">
          <stringProp name="JSONPostProcessor.referenceNames">{escape(varname)}</stringProp>
          <stringProp name="JSONPostProcessor.jsonPathExprs">{escape(jsonpath)}</stringProp>
          <stringProp name="JSONPostProcessor.match_numbers">1</stringProp>
          <stringProp name="JSONPostProcessor.defaultValues">{escape(default)}</stringProp>
        </JSONPostProcessor>
        <hashTree/>
'''


def close_tree(indent: int = 6) -> str:
    """关闭一个 hashTree（与 thread_group / http_sampler 配对）"""
    return " " * indent + "</hashTree>\n"
