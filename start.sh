if [ $# -ne 1 ]

	# 如果没有传入一个参数运行
	
then
	echo "请传入一个启动参数，格式为：author=作者名字"
else

	# 构建爬虫镜像

	docker images | grep poems_crawler

	if [ $? -ne 0 ]
	then
		echo "\n\n\n开始构建爬虫镜像......\n\n\n"

		docker build -t poems_crawler:latest .

		while [ $? -ne 0 ]
		do
			echo "\n\n\n构建爬虫镜像失败！尝试重新构建......\n\n\n"

			docker build -t poems_crawler:latest .
		done

		echo "\n\n\n构建爬虫镜像成功！\n\n\n"
	fi


	if [ $? -eq 0 ]
	then
		# 启动redis服务

		echo "\n\n\n开始启动Redis服务......\n\n\n"

		docker ps -a | grep poems_redis

		if [ $? -ne 0 ]

		# 如果当前还没有redis服务的容器存在，则新创建并放入后台运行

		then
			echo "\n\n\n开始创建并启动Redis服务......\n\n\n"

			docker run -d \
				   --name poems_redis \
				   --restart unless-stopped \
				   --network host \
				   --env TZ=Asia/Shanghai \
				   -v $PWD/redis_data:/data \
				   -u $(id -u ${USER}):$(id -g ${USER}) redis:6.2

			while [ $? -ne 0 ]
			do
				echo "\n\n\n启动Redis服务失败！尝试重新创建并启动......\n\n\n"

				docker run -d \
					   --name poems_redis \
					   --restart unless-stopped \
					   --network host \
					   --env TZ=Asia/Shanghai \
					   -v $PWD/redis_data:/data \
					   -u $(id -u ${USER}):$(id -g ${USER}) redis:6.2
			done

			echo "\n\n\n启动Redis服务成功！\n\n\n"

		else
			docker ps | grep poems_redis

			if [ $? -ne 0 ]

			# 如果redis容器存在但是处于停止状态，则重新启动

			then
				echo "\n\n\n重新启动Redis服务......\n\n\n"

				docker restart poems_redis

				while [ $? -ne 0 ]
				do
					echo "\n\n\n启动Redis服务失败！尝试重新启动......\n\n\n"

					docker restart poems_redis
				done

				echo "\n\n\n启动Redis服务成功！\n\n\n"

			else
				echo "\n\n\nRedis服务正在运行......\n\n\n"
			fi
		fi

		# 启动mongodb服务

		echo "\n\n\n开始启动MongoDB服务......\n\n\n"

		docker ps -a | grep poems_mongodb

		if [ $? -ne 0 ]

			# 如果当前还没有mongodb服务的容器存在，则新创建并放入后台运行

		then
			echo "\n\n\n开始创建并启动MongoDB服务\n\n\n"

			docker run -d \
				   --name poems_mongodb \
				   --restart unless-stopped \
				   --network host \
				   --env TZ=Asia/Shanghai \
				   --env MONGO_INITDB_ROOT_USERNAME=root \
				   --env MONGO_INITDB_ROOT_PASSWORD=123456 \
				   -v $PWD/mongo_data:/data/db \
				   -u $(id -u ${USER}):$(id -g ${USER}) mongo:4.4

			while [ $? -ne 0 ]
			do
				echo "\n\n\n启动MongoDB服务失败！尝试重新启动......\n\n\n"

				docker run -d \
					   --name poems_mongodb \
					   --restart unless-stopped \
					   --network host \
					   --env TZ=Asia/Shanghai \
					   --env MONGO_INITDB_ROOT_USERNAME=root \
					   --env MONGO_INITDB_ROOT_PASSWORD=123456 \
					   -v $PWD/mongo_data:/data/db \
					   -u $(id -u ${USER}):$(id -g ${USER}) mongo:4.4
			done

			echo "\n\n\n启动MongoDB服务成功！\n\n\n"

		else
			docker ps | grep poems_mongodb

			if [ $? -ne 0 ]

				# 如果mongodb容器存在但是处于停止状态，则重新启动

			then
				echo "\n\n\n重新启动MongoDB服务......\n\n\n"

				docker restart poems_mongodb

				while [ $? -ne 0 ]
				do
					echo "\n\n\n启动MongoDB服务失败！尝试重新启动......\n\n\n"

					docker restart poems_mongodb
				done

				echo "\n\n\n启动MongoDB服务成功！\n\n\n"
			else
				echo "\n\n\nMongoDB服务正在运行......\n\n\n"
			fi
		fi

		# 启动mongo-express服务

		echo "\n\n\n开始启动Mongo-express服务......\n\n\n"

		docker ps -a | grep poems_mongo-express

		if [ $? -ne 0 ]

			# 如果当前还没有Mongo-express容器存在，则新创建并放入后台运行

		then
			echo "\n\n\n开始创建并启动Mongo-express服务\n\n\n"

			docker run -d \
				   --name poems_mongo-express \
				   --restart unless-stopped \
				   --network host \
				   --env TZ=Asia/Shanghai \
				   --env ME_CONFIG_MONGODB_SERVER=127.0.0.1 \
				   --env ME_CONFIG_MONGODB_ADMINUSERNAME=root \
				   --env ME_CONFIG_MONGODB_ADMINPASSWORD=123456 \
				   -u $(id -u ${USER}):$(id -g ${USER}) mongo-express:0.54

			while [ $? -ne 0 ]
			do
				echo "\n\n\n启动Mongo-express服务失败！尝试重新启动......\n\n\n"

				docker run -d \
					   --name poems_mongo-express \
					   --restart unless-stopped \
					   --network host \
					   --env TZ=Asia/Shanghai \
					   --env ME_CONFIG_MONGODB_SERVER=127.0.0.1 \
					   --env ME_CONFIG_MONGODB_ADMINUSERNAME=root \
					   --env ME_CONFIG_MONGODB_ADMINPASSWORD=123456 \
					   -u $(id -u ${USER}):$(id -g ${USER}) mongo-express:0.54
			done

			echo "\n\n\n启动Mongo-express服务成功！\n\n\n"
		else
			docker ps | grep poems_mongo-express

			if [ $? -ne 0 ]

				# 如果Mongo-express容器存在但处于停止状态，则重新启动

			then

				echo "\n\n\n重启启动Mongo-express服务......\n\n\n"

				docker restart poems_mongo-express

				while [ $? -ne 0 ]
				do
					echo "\n\n\n启动Mongo-express服务失败！尝试重新启动......\n\n\n"

					docker restart poems_mongo-express
				done

				echo "\n\n\n启动Mongo-express服务成功！\n\n\n"
			else
				echo "\n\n\nMongo-express服务正在运行......\n\n\n"
			fi

		fi

		# 启动爬虫

		echo "\n开始爬取 【$1】的诗文......\n\n\n"


		docker run --rm \
			   --name poems_crawler \
			   --network host \
			   --env TZ=Asia/Shanghai \
			   -v $PWD/zhsc_crawler:/app \
			   -u $(id -u ${USER}):$(id -g ${USER}) poems_crawler:latest $1

		if [ $? -eq 0 ]
		then
			echo "\n\n\n爬取数据成功！"
		else
			echo "\n\n\n爬取数据失败！请输入正确参数，格式：author=[作者名]"
		fi

		# 清理后台Redis、MongoDB和Mongo-express服务

		echo "\n\n\n清理后台Redis、MongoDB和Mongo-express服务......\n\n\n"
		docker stop poems_redis poems_mongodb poems_mongo-express
		docker container rm poems_redis poems_mongodb poems_mongo-express
	fi

fi
