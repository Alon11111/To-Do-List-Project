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
    // alert("Add succesful");
    console.log("ADD RESPONSE:\t", addRes);
  };

  const editBtnClickHandler = (row) => {
    return (
      <>
        <input
          ref={editDescriptionRef}
          type="text"
          defaultValue={row.description}
        />
        <input ref={editDateRef} type="date" defaultValue={row.date} />
        <div className="update">
          <a onClick={() => submitUpdate(row)}>Save</a>
        </div>
      </>
    );
  };

  const displayDefaultTaskRow = (row) => {
    return (
      <>
        <div className="description">{row.description}</div>
        <div className="date">{row.date}</div>
        <div className="update">
          <a onClick={() => setEditRowId(row.task_id)}>Update</a>
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
      status: "Done",
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
        <header>
          <div className="Nav">
            <div className="name">
              <a>{name}'s To Do List</a>
            </div>
            <div className="task-view-buttons">
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
                  currentTaskView === "Done" ? "button active" : "button"
                }
                onClick={() => handleCurrentTaskViewChange("Done")}
              >
                Done
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
            <form className="searchContainer" onSubmit={handleSearchSubmit}>
              <input
                ref={searchQueryRef}
                type="text"
                name="description"
                placeholder="Search task here.."
                className="searchInput"
                required
              />
              <input
                type="submit"
                value="Search"
                className="searchBtn"
                id="searchBtnInput"
              />
            </form>
            <div className="logOut">
              <button onClick={() => clearSessionBtn()}>Log-Out</button>
            </div>
          </div>
        </header>

        {/* <div className="title" id="add">
          <h1 className="Title">Add Task</h1>
        </div> */}
        <div className="add">
          <form className="addContainer" onSubmit={addHandler}>
            <input
              type="text"
              name="description"
              placeholder="Add new task's description here.."
              className="description"
              ref={addDescriptionRef}
              required
            />
            <input
              type="date"
              name="date"
              placeholder="date"
              className="date"
              ref={addDateRef}
              required
            />
            <input type="submit" value="Add" className="addBtn" />
          </form>
        </div>
        {/* <div className="title" id="tasks">
          <h1 className="Title">{name}'s Tasks</h1>
        </div> */}
        <div className="tasks">
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
                // @@@@@@@@@@@@@@
                <div className={`task ${row.status}`} key={key}>
                  {row.status === "In-Progress" ? (
                    <div className="done">
                      <a onClick={() => doneBtnClickHandler(row)}>Done</a>
                    </div>
                  ) : (
                    <div className={row.status === "Done" ? "unDone" : "retry"}>
                      <a onClick={() => unDoneBtnClickHandler(row)}>
                        {row.status === "Done" ? "UnDone" : "Retry"}
                      </a>
                    </div>
                  )}
                  <div className="status">{row.status}</div>

                  {row.task_id == editRowId
                    ? editBtnClickHandler(row)
                    : displayDefaultTaskRow(row)}

                  <div className="delete">
                    <a onClick={() => deleteBtnClickHandler(row)}>Delete</a>
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
