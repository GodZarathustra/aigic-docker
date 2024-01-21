import json

from pyxxl import ExecutorConfig, PyxxlRunner

with open("config.json", 'r') as file:
    data = json.load(file)


config = ExecutorConfig(
    xxl_admin_baseurl=data['xxl_admin_baseurl'],
    executor_app_name=data['executor_app_name'],
    executor_host=data['executor_host'],
    executor_server_host=data['executor_server_host'],
    access_token=data['access_token'],
    executor_port=data['executor_port'],
    miner_id=data['miner_id'],
)

app = PyxxlRunner(config)


@app.handler.register(name="aipaint")
def test_task3():
    # g.logger.info("get executor params: %s" % g.xxl_run_data.executorParams)
    # return ai_paint(g.xxl_run_data.executorParams)
    pass


app.run_executor()