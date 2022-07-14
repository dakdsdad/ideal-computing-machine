/*
 * Copyright (c) 2006-2020, RT-Thread Development Team
 *
 * SPDX-License-Identifier: Apache-2.0
 *
 * Change Logs:
 * Date           Author       Notes
 * 2020-04-05     bigmagic    first version
 */

#include <rtthread.h>

int main(int argc, char **argv)
{
	rt_kprintf("Hi, this is RT-Thread!!\n");
	// msh_exec("uart4_data",rt_strlen("uart4_data"));
	while (1)
	{
		rt_thread_sleep(500);
		// msh_exec("web_post_test",rt_strlen("web_post_test"));
	}
	return 0;
}
