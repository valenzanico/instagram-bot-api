const instaTouch = require("instatouch");

(async () => {
  try {
    let args = process.argv.slice(2);
    let users = [];
    const POST = args[0];
    const SESSION_ID = args[1];
    const NUMBER = parseInt(args[2]);
    const START_FROM = parseInt(args[3]);
    const options = {
      count: START_FROM + NUMBER,
      session: SESSION_ID,
    };
    var likers = await instaTouch.likers(POST, options);
    likers.collector.forEach((user, index) => {
      if (index > START_FROM) {
        if (user.is_private == false) {
          delete user.id;
          delete user.full_name;
          delete user.profile_pic_url;
          users.push(user);
        }
      }
    });
    process.stdout.write(JSON.stringify(users));
  } catch (error) {
    console.log(error);
  }
})();
