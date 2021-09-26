import db from '../firebase.config';
import { Calendar, Badge } from 'antd';
import { collection, getDocs } from 'firebase/firestore/lite';

async function getTeams() {
    // Teams
    const res = collection(db, 'teams');
    const data = await getDocs(res);
    const teams = data.docs.map(doc => doc.data());

    // Users
    const usersRaw = collection(db, 'users')
    const usersData = await getDocs(usersRaw);
    const users = usersData.docs.map(doc => doc.data());

    // Breaks
    const breaksRaw = collection(db, 'breaks')
    const breakData = await getDocs(breaksRaw);
    const breaks = breakData.docs.map(doc => doc.data());

    // Weekly meetings
    const weeklyMeetingsRaw = collection(db, 'weekly_meetings')
    const weeklyMeetingsData = await getDocs(weeklyMeetingsRaw);
    const weeklyMeetings = weeklyMeetingsData.docs.map(doc => doc.data());

    console.log(teams)
    console.log(users)
    console.log(breaks);
    console.log(weeklyMeetings);
  
}

function getListData(value) {

    getTeams();

    let listData;
    switch (value.date()) {
        case 8:
            listData = [
                { type: 'warning', content: 'This is warning event.' },
                { type: 'success', content: 'This is usual event.' },
            ];
            break;
        case 10:
            listData = [
                { type: 'warning', content: 'This is warning event.' },
                { type: 'success', content: 'This is usual event.' },
                { type: 'error', content: 'This is error event.' },
            ];
            break;
        case 15:
            listData = [
                { type: 'warning', content: 'This is warning event' },
                { type: 'success', content: 'This is very long usual event。。....' },
                { type: 'error', content: 'This is error event 1.' },
                { type: 'error', content: 'This is error event 2.' },
                { type: 'error', content: 'This is error event 3.' },
                { type: 'error', content: 'This is error event 4.' },
            ];
            break;
        default:
    }
    return listData || [];
}

function dateCellRender(value) {
    const listData = getListData(value);
    return (
        <ul className="events">
            {listData.map(item => (
                <li key={item.content}>
                    <Badge status={item.type} text={item.content} />
                </li>
            ))}
        </ul>
    );
}

function getMonthData(value) {
    if (value.month() === 8) {
        return 1394;
    }
}

function monthCellRender(value) {
    const num = getMonthData(value);
    return num ? (
        <div className="notes-month">
            <section>{num}</section>
            <span>Backlog number</span>
        </div>
    ) : null;
}

function Calend() {
    return (
        <Calendar dateCellRender={dateCellRender} monthCellRender={monthCellRender} />
    )
}

export default Calend;