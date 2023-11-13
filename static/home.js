const Home = () => {
  const [data, setData] = React.useState(null);
  const [name, setName] = React.useState(null);
  const addDescriptionRef = React.useRef(null);
  const addDateRef = React.useRef(null);
  const [currentTaskView, setCurrentTaskView] = React.useState("In-Progress");
  const [editRowId, setEditRowId] = React.useState(null);
  const editDescriptionRef = React.useRef(null);
  const editDateRef = React.useRef(null);
  const [searchQuery, setSearchQuery] = React.useState(null);
  const searchQueryRef = React.useRef(null);

  const getTasks = async () => {
    const response = await axios.get("/read_tasks");
    setData(response.data);
  };

  const getName = async () => {
    const response = await axios.get("/read_name");
    setName(response.data);
  };

  React.useEffect(() => {
    getName();
    getTasks();
  }, []);

  const clearSessionBtn = async () => {
    await axios.get("/log_out");
    window.location.href = "/login";
  };

  const addHandler = async () => {
    const addTask = {
      description: addDescriptionRef.current.value,
      date: addDateRef.current.value,
    };
    const addRes = await axios.post("/add_task", addTask);
    window.location.href = "/";
    console.log("ADD RESPONSE:\t", addRes);
  };

  const editBtnClickHandler = (row) => {
    return (
      <>
        <input
          ref={editDescriptionRef}
          type="text"
          maxlength="75"
          defaultValue={row.description}
          className="edit-description-container"
        />
        <input
          ref={editDateRef}
          type="date"
          defaultValue={row.date}
          className="edit-date-container"
        />
        <div className="save-update-btn">
          <img
            src="static/images/save.png"
            title="Click here to Save task changed values"
            className="save-img"
            onClick={() => submitUpdate(row)}
          />
        </div>
      </>
    );
  };

  const displayDefaultTaskRow = (row) => {
    return (
      <>
        <div className="task-description">{row.description}</div>
        <div className="task-date">{row.date}</div>
        <div className="task-update-btn">
          <img
            src="static/images/edit.png"
            className="edit-img"
            title="Click here to Edit task values"
            onClick={() => setEditRowId(row.task_id)}
          />
        </div>
      </>
    );
  };

  const submitUpdate = async (row) => {
    const updatedTask = {
      task_id: row.task_id,
      description: editDescriptionRef.current.value,
      date: editDateRef.current.value,
    };
    const updateRes = await axios.post("/update_task", updatedTask);
    await getTasks();
    console.log("UPDATE RESPONSE:\t", updateRes);
    setEditRowId(null);
  };

  const doneBtnClickHandler = async (row) => {
    const taskStatus = {
      task_id: row.task_id,
      status: "Finished",
      date: row.date,
    };
    await axios.post("/update_status", taskStatus);
    await getTasks();
    console.log("STATUS RESPONSE:\t", "DONE");
  };

  const unDoneBtnClickHandler = async (row) => {
    const taskStatus = {
      task_id: row.task_id,
      status: "In-Progress",
      date: row.date,
    };
    await axios.post("/update_status", taskStatus);
    await getTasks();
    console.log("STATUS RESPONSE:\t", "BACK TO IN PROGRESS");
  };

  const deleteBtnClickHandler = async (row) => {
    const deleteTask = {
      task_id: row.task_id,
    };
    await axios.post("/delete_task", deleteTask);
    await getTasks();
    console.log("DELETE RESPONSE:\t", "DELETED");
  };

  const handleCurrentTaskViewChange = (newTaskView) => {
    searchQueryRef.current.value = "";
    setSearchQuery(null);
    setCurrentTaskView(newTaskView);
  };

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    setSearchQuery(searchQueryRef.current.value);
    setCurrentTaskView(null);
  };

  const displayList = () => {
    if (!data) return <></>;
    return (
      <>
        <div className="header-container">
          <div className="header-content">
            <h2 className="first-name">{name}'s tasks:</h2>
            <div className="nav-container">
              <button
                className={
                  currentTaskView === "All" ? "button active" : "button"
                }
                onClick={() => handleCurrentTaskViewChange("All")}
              >
                All
              </button>
              <button
                className={
                  currentTaskView === "In-Progress" ? "button active" : "button"
                }
                onClick={() => handleCurrentTaskViewChange("In-Progress")}
              >
                In-Progress
              </button>
              <button
                className={
                  currentTaskView === "Finished" ? "button active" : "button"
                }
                onClick={() => handleCurrentTaskViewChange("Finished")}
              >
                Finished
              </button>
              <button
                className={
                  currentTaskView === "Expired" ? "button active" : "button"
                }
                onClick={() => handleCurrentTaskViewChange("Expired")}
              >
                Expired
              </button>
            </div>
            <div className="search-container">
              <form className="search-content" onSubmit={handleSearchSubmit}>
                <input
                  ref={searchQueryRef}
                  type="text"
                  name="description"
                  placeholder="Search.."
                  className="search-field"
                  required
                />
                <img src="static/images/search.png" className="search-img" />
              </form>
            </div>
            <div className="logout-container">
              <button onClick={() => clearSessionBtn()}>Log-Out</button>
            </div>
          </div>
          <div className="add-container">
            <form className="add-content" onSubmit={addHandler}>
              <div className="add-title-container">
                <h2 className="add-title">Add New Task</h2>
              </div>
              <textarea
                name="description"
                maxLength="75"
                placeholder="Add new task's description here.."
                className="add-description"
                ref={addDescriptionRef}
                required
              />
              <input
                type="date"
                name="date"
                placeholder="date"
                className="add-date"
                ref={addDateRef}
                required
              />
              <input type="submit" value="Add" className="add-btn" />
            </form>
          </div>
        </div>
        <div className="tasks-container">
          <div className="titles">
            <h2 className="status-title">Status</h2>
            <h2 className="description-title">Description</h2>
            <h2 className="date-title">Date</h2>
          </div>
          {data
            .filter(
              searchQuery === null
                ? (row) =>
                    currentTaskView === "All" || row.status === currentTaskView
                : (row) =>
                    row.description
                      .toLowerCase()
                      .includes(searchQuery.toLowerCase())
            )
            .map((row, key) => {
              return (
                <div className="task-container" key={key}>
                  {row.status === "In-Progress" ? (
                    <div className="done-btn-container">
                      <img
                        src="static/images/done.png"
                        className="done-img"
                        title="Click here to Finish task"
                        onClick={() => doneBtnClickHandler(row)}
                      />
                    </div>
                  ) : (
                    <div
                      className={
                        row.status === "Finished"
                          ? "undone-btn-container"
                          : "retry-btn-container"
                      }
                    >
                      <img
                        src={
                          row.status === "Finished"
                            ? "static/images/undone.png"
                            : "static/images/retry.png"
                        }
                        className={
                          row.status === "Finished" ? "undone-img" : "retry-img"
                        }
                        title={
                          row.status === "Finished"
                            ? "Click here to Undo finish task"
                            : "Click here to Retry doing task in time (update to today's date automatically)"
                        }
                        onClick={() => unDoneBtnClickHandler(row)}
                      />
                    </div>
                  )}
                  <div className={`status-container ${row.status}`}>
                    {row.status}
                  </div>

                  {row.task_id == editRowId
                    ? editBtnClickHandler(row)
                    : displayDefaultTaskRow(row)}

                  <div className="delete-btn-container">
                    <img
                      src="static/images/delete.png"
                      className="delete-img"
                      title="Click here to Delete task"
                      onClick={() => deleteBtnClickHandler(row)}
                    />
                  </div>
                </div>
              );
            })}
        </div>
      </>
    );
  };

  return <>{displayList()}</>;
};

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<Home />);
